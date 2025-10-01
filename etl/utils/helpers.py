def extraer_subtabla(df, inicio_texto, fin_texto):
    fila_inicio = df.index[df.apply(lambda r: r.astype(str).str.strip().str.upper().eq(inicio_texto.upper()).any(), axis=1)][0]
    fila_fin = df.index[df.apply(lambda r: r.astype(str).str.strip().str.upper().eq(fin_texto.upper()).any(), axis=1)][0]
    subtabla = df.loc[fila_inicio+2:fila_fin-2].dropna(how="all", axis=1).copy()
    
    return subtabla