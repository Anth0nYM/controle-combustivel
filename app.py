import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pages.input import page_two

# Função para carregar os dados do st.session_state
def load_data():
    if 'df' in st.session_state:
        df = st.session_state.df
        # Verifica se a coluna 'Data' existe e tenta converter para datetime se houver dados
        if 'Data' in df.columns and not df['Data'].empty:
            try:
                df['Data'] = pd.to_datetime(df['Data'])
            except ValueError as e:
                st.error(f"Erro ao converter coluna 'Data': {str(e)}")
        return df
    else:
        return pd.DataFrame(columns=['Placa', 'Quilometragem', 'Quantidade', 'Cupom', 'Data', 'Valor', 'Obra'])

# Configurando a página principal
def main_page():
    st.title('Relatórios')
    # Carregar os dados do st.session_state
    df = load_data()

    if not df.empty:
        # Gráfico de gastos por placa
        fig, ax = plt.subplots()
        df.groupby('Placa')['Valor'].sum().sort_values(ascending=False).plot(kind='bar', ax=ax)
        ax.set_title('Gastos Totais por Placa')
        ax.set_ylabel('Valor (Reais)')
        st.pyplot(fig)

        # Encontrar a placa que mais gastou em um determinado mês
        st.sidebar.subheader('Filtro por Mês')
        selected_month = st.sidebar.selectbox('Selecione o Mês', df['Data'].dt.to_period('M').unique().astype(str))

        # Filtrar os dados pelo mês selecionado
        df_filtered = df[df['Data'].dt.to_period('M') == selected_month]

        if not df_filtered.empty:
            # Placa que mais gastou no mês selecionado
            top_plate = df_filtered.groupby('Placa')['Valor'].sum().idxmax()
            st.write(f"A placa que mais gastou em {selected_month} foi: **{top_plate}**")

# Seleção da página
page = st.sidebar.selectbox('Selecione a Página', ('main', 'input'))

if page == 'main':
    main_page()
else:
    page_two()
