import duckdb
con = duckdb.connect("data/db/staging.duckdb")
cols = [c[0] for c in con.execute("DESCRIBE staged_tcga_clinical").fetchall()]
print("Clinical columns available:")
print([c for c in cols if "AGE" in c or "STATUS" in c or "MONTHS" in c])
con.close()