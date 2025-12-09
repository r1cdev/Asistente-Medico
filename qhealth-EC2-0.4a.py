 # Importing required packages
import streamlit as st
import openai
import uuid
import time
import pandas as pd
import io
from openai import OpenAI

# 1. Initialize OpenAI client
client = openai
openai.api_key = "your openai api key"

# 2. Your chosen model
MODEL = "gpt-4-turbo-preview"

# 3. Initial page config
st.set_page_config(
     page_title='Asistente Médico',
     layout="wide",
     initial_sidebar_state="expanded",
)

# 4. Initialize session state variables
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "run" not in st.session_state:
    st.session_state.run = {"status": None}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retry_error" not in st.session_state:
    st.session_state.retry_error = 0

if "sintomas" not in st.session_state:
    st.session_state.sintomas = ""

if "proceso" not in st.session_state:
    st.session_state.proceso = ""

if "diagnostico_txt" not in st.session_state:
    st.session_state.diagnostico_txt = ""
    
if "tratamiento_txt" not in st.session_state:
    st.session_state.tratamiento_txt = ""


# 5. Set up the sidebar
with st.sidebar:
    st.image("quantum.jpg")
    st.text("")
    st.header(":blue[Asistente Médico 1er. Nivel]", divider="blue", )
    st.markdown("*Versión POC - 0.4*")
    
    with st.container(height=None, border=1):
        diagnostico = st.button("Diagnóstico Diferencial")
        if diagnostico:
            st.session_state.proceso = "Diagnostico"
        tratamiento = st.button("Plan de Tratamiento")
        if tratamiento:
            st.session_state.proceso = "Tratamiento"
    
    reiniciar = st.button("Re-Iniciar")
    if reiniciar:
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
        
    st.divider()
   
            

# 6. Area para Captura de Diagnóstico
with st.container(height=None, border=1):
    st.title("Análisis de Paciente")
    st.markdown(":blue[Incluya edad, sexo, antecedentes médicos relevantes, medicamentos, síntomas presentes, síntomas asociados, descripciones de estudios relevantes (incluidos laboratorios e imágenes), el curso de la enfermedad y cualquier información adicional  que pueda incluir al consultar a otro médico sobre su paciente.]")
    
    sintomas = st.text_area(
        label = "**Introduzca los sintomas del paciente:**", 
        height=150, 
        key="sintomas", 
        #max_chars = 1000 , 
        placeholder="Síntomas"
    )
    st.markdown("*Los borradores de diferenciales y planes brindan información que un médico puede considerar pero que nunca debe reemplazar su juicio. La información de identificación protegida no debe ingresarse en Quantum Health. Todos los resúmenes de pacientes deben ser anónimos.*")


placeholder1 = st.empty()

with placeholder1.container():
    col1, col2, = st.columns(2)
    with col1:
        st.header("Diagnóstico")
    with col2:
        st.header("Tratamiento")
    
    
# 7. Get OpenAI Assistant ID and create the thread when assistant not in st.session_state
if "assistant" not in st.session_state:
    openai.api_key = "your openai key"
    st.session_state.assistant = openai.beta.assistants.retrieve("your openai assistant key")
    st.session_state.thread = client.beta.threads.create(
        metadata={'session_id': st.session_state.session_id}
    ) 


# 8. Display chat messages when assistant in st.session_state
elif hasattr(st.session_state.run, 'status') and st.session_state.run.status == "completed":
    st.session_state.messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread.id,
        limit = 1
    )
    
 
    for message in reversed(st.session_state.messages.data):
        #with st.chat_message(message.role):
                        
        for content_part in message.content:
            message_text = content_part.text.value
            #st.markdown(st.session_state.proceso)    
            #st.markdown(message_text)
            if st.session_state.proceso == "Diagnostico":
                st.session_state.diagnostico_txt = message_text
                #st.markdown(diagnostico_txt)
                
            if st.session_state.proceso == "Tratamiento":
                st.session_state.tratamiento_txt = message_text
                #st.markdown(tratamiento_txt)
    
    with col1:
        st.markdown(st.session_state.diagnostico_txt)
    with col2:
        st.markdown(st.session_state.tratamiento_txt)
            
    
# 9. Procesa el Diagnóstico Diferencial
if  diagnostico:
    prompt = "Da el  diagnóstico del paciente con los siguientes sintomas: " + sintomas
    diagnostico = False
    
    
    with st.sidebar:
        st.write("Ejecutando Diagnóstico Diferencial...")
        st.status("Procesando...") 

    message_data = {
        "thread_id": st.session_state.thread.id,
        "role": "user",
        "content": prompt
    }

    st.session_state.messages = client.beta.threads.messages.create(**message_data)

    st.session_state.run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant.id,
    )
    if st.session_state.retry_error < 3:
        time.sleep(1)
        st.rerun()

# 10. Display Procesa el Plan de Tratamiento
if  tratamiento:
    prompt = "Tomando diagnóstico del paciente que ya respondiste anteriormente, responde con un plan de tratamiento" 
    tratamiento = False
    placeholder1.empty()
    
   
    with st.sidebar:
        st.write("Ejecutando Plan de Tratamiento...")
        st.status("Procesando...") 
    
    
    message_data = {
        "thread_id": st.session_state.thread.id,
        "role": "user",
        "content": prompt
    }

    st.session_state.messages = client.beta.threads.messages.create(**message_data)

    st.session_state.run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant.id,
    )
    if st.session_state.retry_error < 3:
        time.sleep(1)
        st.rerun()

# Handle run status
if hasattr(st.session_state.run, 'status'):
    
    if st.session_state.run.status == "running":
        #with st.chat_message('assistant'):
        #    st.write("Thinking ......")
        if st.session_state.retry_error < 3:
            time.sleep(1)
            st.rerun()

    elif st.session_state.run.status == "failed":
        st.session_state.retry_error += 1
        #with st.chat_message('assistant'):
        if st.session_state.retry_error < 3:
            st.write("Run failed, retrying ......")
            time.sleep(3)
            st.rerun()
        else:
            st.error("FAILED: The OpenAI API is currently processing too many requests. Please try again later ......")

    elif st.session_state.run.status != "completed":
        st.session_state.run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread.id,
            run_id=st.session_state.run.id,
        )
        if st.session_state.retry_error < 3:
            time.sleep(3)
            st.rerun()