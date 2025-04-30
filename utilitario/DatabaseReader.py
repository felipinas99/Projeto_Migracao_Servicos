import psycopg2
from psycopg2 import sql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def connect_to_db(host, database, user, password, port):
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    return conn

def get_tables_and_columns(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'intranet'
    """)
    tables_columns = cursor.fetchall()
    cursor.close()
    return tables_columns

def associate_data(tables_columns):
    table_column_pairs = [f"{table}.{column}" for table, column in tables_columns]
    
    if not table_column_pairs:
        raise ValueError("No table and column pairs found.")
    
    vectorizer = TfidfVectorizer(stop_words=None)  # Disable stop word removal
    vectors = vectorizer.fit_transform(table_column_pairs).toarray()
    cosine_matrix = cosine_similarity(vectors)
    
    associations = {}
    for idx, pair in enumerate(table_column_pairs):
        similar_indices = cosine_matrix[idx].argsort()[:-5:-1]
        similar_items = [(table_column_pairs[i], cosine_matrix[idx][i]) for i in similar_indices if i != idx]
        associations[pair] = similar_items
    
    return associations

def main():
    conn = connect_to_db('localhost', 'Intranet', 'postgres', 'admin', '5432')
    tables_columns = get_tables_and_columns(conn)
    
    # Debugging statement to check the fetched tables and columns
    print(f"Fetched tables and columns: {tables_columns}")
    
    if not tables_columns:
        print("No tables and columns found in the database.")
        return
    
    associations = associate_data(tables_columns)
    
    for table_column, similar_items in associations.items():
        print(f"{table_column}:")
        for item, score in similar_items:
            print(f"  {item} (similarity: {score:.2f})")
    
    conn.close()

if __name__ == "__main__":
    main()