import pandas as pd 
import streamlit as st
import options as opt
from pandas_datareader import data
from func_pyeconomics import  graf_plotly
import plotly.graph_objects as go

### ========= ARQUITETURA DA PÁGINA ========= ###


### ==== FUNÇÃO PARA CRIAR PÁGINA DE ANÁLISE DE CARTEIRA ==== ###

def pag_carteira():
# ESCOLHENDO ATIVOS PARA ENTRAR NA CARTEIRA
    period = st.sidebar.slider('select',2000,2022,(2015,2022))
    