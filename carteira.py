import pandas as pd 
import numpy as np 
import streamlit as st
import options as opt
from pandas_datareader import data
from func_pyeconomics import  graf_plotly, gera_carteira, normaliza_carteira, graf_corr
import plotly.graph_objects as go
import plotly.express as px 
import seaborn as sns 
import matplotlib.pyplot as plt


### ==== FUNÇÃO PARA CRIAR PÁGINA DE ANÁLISE DE CARTEIRA ==== ###

def pag_carteira():
# ESCOLHENDO ATIVOS PARA ENTRAR NA CARTEIRA
    stocks_csv = pd.read_csv('base_csv/stocks.csv')
    stocks = st.sidebar.multiselect('Insira o ticker das ações na carteira:',stocks_csv)
    period = st.sidebar.slider('A partir de qual ano deseja analisar?:',2010,2021,(2010))
    n_stocks = len(stocks)  
    st.write(
        'Nesta página você poderá realizar a simulação de uma carteira de ações e compará-la com o benchmark (Ibovespa). Basta escolher os ativos e o período inicial na barra lateral. Os dados são extraídos de diversas fontes, sendo a fonte principal o YAHOO FINANCE. Também será realizada diversas análises referente ao portfólio.'
    )
    st.sidebar.write(
        'Coloque o peso que cada ativo terá na carteira'
    )
    peso = []
    for i in range(0,n_stocks):
        ps = st.sidebar.number_input(f'Peso do ativo {stocks[i]}',0,100,key=f'peso_{i}')
        peso.append(ps/100)
    if (sum(peso) != 1) & (n_stocks > 0):
        st.sidebar.write('A soma dos pesos tem que ser de 100%')
    elif (sum(peso) == 1):
        if st.sidebar.button('Gerar Carteira'):
            ### ========= ARQUITETURA DA PÁGINA ========= ### 

            ### ========= COMPARATIVO CARTEIRA X IBOVESPA ========= ### 
            st.markdown(
                '***COMPARATIVO - CARTEIRA X IBOVESPA***'
            )
            dataframe = gera_carteira(stocks,period)
            df_norm = normaliza_carteira(dataframe)
            df_norm.rename(columns={'^BVSP':'IBOVESPA'}, inplace=True)
            benchmark = pd.DataFrame(df_norm['IBOVESPA'])
            carteira = df_norm.drop(columns='IBOVESPA')
            carteira = carteira * peso
            carteira['CARTEIRA'] = carteira.sum(axis=1)
            cart = pd.DataFrame(carteira['CARTEIRA'])
            cart_bench = pd.concat([cart, benchmark], axis = 1)
            ativos_ibov = pd.concat([carteira, benchmark], axis = 1)
            st.write(graf_plotly(cart_bench))
            st.markdown('***COMPARATIVO - ATIVOS X IBOVESPA***')
            st.write(graf_plotly(df_norm))

            ### ========= CORRELAÇÃO ENTRE OS ATIVOS ========= ###
            st.markdown('***CORRELAÇÃO ENTRE OS ATIVOS***')
            retorno_ativos = ((df_norm / df_norm.shift(1)) - 1).dropna()
            correlacao = retorno_ativos.corr()
            st.write(graf_corr(correlacao))

            ### ========= CALCULANDO O RETORNO DE UM PORTFÓLIO ========= ###
            retorno_carteira = ((cart/cart.shift(1))-1)
            retorno_benchmark = ((benchmark/benchmark.shift(1))-1)
            st.markdown('***TAXA DE RETORNO DIÁRIO DA CARTEIRA***')
            st.write(graf_plotly((retorno_carteira*100)))
            
            ### ========= CALCULANDO A VARIÂNCIA E O DESVIO PADRÃO DO PORTFÓLIO ========= ###
            st.markdown('***VARIÂNCIA, VOLATILIDADE E SHARPE RATIO DA CARTEIRA***')
            weights = np.array(peso)
            cov_ativos = retorno_ativos.drop(columns='IBOVESPA').cov()*246
            pfolio_var = np.dot(weights.T, np.dot(cov_ativos,weights))
            pfolio_vol = pfolio_var**0.5  
            pfolio_sharpe = (retorno_carteira.mean() / pfolio_vol)*np.sqrt(246)*100

            benchmark_var = benchmark.var()
            benchmark_vol = benchmark_var**0.5
            benchmark_sharpe = (retorno_benchmark.mean() / benchmark_vol)*np.sqrt(246)*100

            st.write(f'A variância do portfólio é {round(pfolio_var*100,2)}%. A variância do Ibovespa é {float(round(benchmark_var*100,2))}%.')
            st.write(f'A volatilidade do portfólio é {round(pfolio_vol*100,2)}%. A volatilidade do Ibovespa é {float(round(benchmark_vol*100,2))}%.')
            st.write(f'O Sharpe Ratio é de {float(round(pfolio_sharpe,2))}. O Sharpe Ratio do Ibovespa é {float(round(benchmark_sharpe,2))}.')
            st.write(retorno_benchmark)
            st.write(retorno_carteira)