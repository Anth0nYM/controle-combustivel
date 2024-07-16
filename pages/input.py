import pandas as pd
from datetime import datetime
import streamlit as st
import os

# Função para carregar ou inicializar o DataFrame
def load_data():
    if os.path.exists('data'):
        csv_path = os.path.join('data', 'abastecimentos.csv')
        if os.path.exists(csv_path):
            try:
                return pd.read_csv(csv_path)
            except pd.errors.EmptyDataError:
                st.warning("O arquivo CSV está vazio.")
                return pd.DataFrame(columns=['Placa', 'Quilometragem', 'Quantidade', 'Cupom', 'Data', 'Valor', 'Obra'])
        else:
            return pd.DataFrame(columns=['Placa', 'Quilometragem', 'Quantidade', 'Cupom', 'Data', 'Valor', 'Obra'])
    else:
        os.makedirs('data')
        return pd.DataFrame(columns=['Placa', 'Quilometragem', 'Quantidade', 'Cupom', 'Data', 'Valor', 'Obra'])

# Função para salvar o DataFrame em um arquivo CSV
def save_data(df):
    if not os.path.exists('data'):
        os.makedirs('data')
    csv_path = os.path.join('data', 'abastecimentos.csv')
    df.to_csv(csv_path, index=False)

# Página para inserção de dados de abastecimento
def page_two():
    if 'df' not in st.session_state:
        st.session_state.df = load_data()

    st.title('Registro de Abastecimento de Veículos')

    # Texto de instruções
    with st.expander("ATENÇÃO. LEIA ANTES DE INSERIR OS DADOS"):
        st.write("""
            **Placa**: A placa do veículo, no formato ABC-1234.\n
            **Quilometragem**: A quilometragem atual do veículo, em quilômetros.\n
            **Quantidade de Litros**: A quantidade de litros de combustível abastecido.\n
            **Número do Cupom Fiscal**: O número do cupom fiscal fornecido no momento do abastecimento.\n
            **Data do Abastecimento**: A data em que o abastecimento foi realizado.\n
            **Quantidade Total em Reais**: O valor total pago pelo abastecimento, em reais.\n
            **Obra do Abastecimento**: A obra associada ao abastecimento.
        """)

    # User Inputs
    placa = st.text_input('Placa')
    quilometragem = st.number_input('Quilometragem (KM)', format="%.2f")
    quantidade = st.number_input('Quantidade (Litros)', format="%.2f")
    cupom = st.text_input('Número do Cupom Fiscal')
    data = st.date_input('Data do Abastecimento', value=datetime.today())
    valor = st.number_input('Valor (Reais)', format="%.2f")
    obra = st.text_input('Obra do Abastecimento')

    # Botão para adicionar registro
    if st.button('Registrar'):
        # Adicionando novo registro ao DataFrame
        new_row = {
            'Placa': placa,
            'Quilometragem': quilometragem,
            'Quantidade': quantidade,
            'Cupom': cupom,
            'Data': data.strftime('%Y-%m-%d'),
            'Valor': valor,
            'Obra': obra
        }
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(st.session_state.df)
        st.success('Registro adicionado com sucesso!')

    # Exibindo o DataFrame
    st.header('Dados de Abastecimento')
    st.write(st.session_state.df)
