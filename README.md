# Asistente Médico
### Prueba de Concepto "POC"  - ***Quantum Health***  
![Static Badge](https://img.shields.io/badge/version-POC_0.4-blue)  

<img src="screen_app.jpg" >  

## Descripción
Esta es una Prueba de Concepto (POC)  para el desarrollo de un asistente médico que utiliza inteligencia artificial (AI) con los siguientes elementos: 
- **Síntomas del paciente**: Como datos de entrada, Incluya edad, sexo, antecedentes médicos relevantes, medicamentos, síntomas presentes, síntomas asociados, descripciones de estudios relevantes (incluidos laboratorios e imágenes), el curso de la enfermedad y cualquier información adicional que pueda incluir al consultar a otro médico sobre su paciente. 
- **Diagnóstico**: Es el resultado que produce la aplicación en base a los síntomas del paciente. Se utiliza como datos de referencia (RAG) el diccionario médico Webster's New World
- **Tratamiento**: Es el resultado que produce la aplicación que sugiere el tratamiento indicado para el paciente en base a los síntomas y el diagnóstico.
<br>
La prueba de concepto del Asistente Médico es una aplicación de Soporte a la Decisión Clínica (CDSS) diseñada para capacitar en los procesos de toma de decisiones clínicas de los médicos. La aplicación genera borradores de diagnósticos diferenciales, evaluaciones y planes, y respuestas a preguntas de referencia clínica. Las respuestas proporcionan la base para recomendaciones específicas sujetas a una revisión independiente por parte del usuario médico. Las respuestas de IA son recomendaciones en forma de borradores que el usuario médico debe revisar en detalle.
<br>

## Limitaciones
Las funciones principales solo deben usarse como complemento del razonamiento médico y nunca reemplazar ni reemplazar el juicio de un médico. La aplicación no está destinada a ser utilizada por pacientes, sino por personal médico. Los usuarios no deben utilizar este modelo para consejos de salud personal o como sustituto de una consulta médica profesional. La aplicación solo ofrece recomendaciones a los médicos que les ayudan en la toma de decisiones clínicas, y las respuestas de IA a menudo requieren la experiencia de un médico para interpretar las respuestas. 

## Características
- Código:  Pyhton
- Plataforma de aplicación:  Streamlit
- Plataforma de AI: OpenAI (Se requiere openai.api_key y openai_assistant_ID)
- model: gpt-4-turbo-preview
- Infraestructura de servicios:  EC2 - AWS
- URL: [POC - Asistente Médico](http://qhealth.homeip.net:8501/)
- Versión: ![Static Badge](https://img.shields.io/badge/version-POC_0.4-blue)
