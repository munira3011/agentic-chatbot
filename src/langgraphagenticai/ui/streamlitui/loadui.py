import streamlit as st
import os

from src.langgraphagenticai.ui.streamlitui.config import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls={}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(),layout="wide")
        st.header("🤖 "+ self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
        

        with st.sidebar:    
            # Get options from Config
            llm_options = self.config.get_llm_options()
            usecase_options= self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            # Model selection
            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠ Please enter your groq API key to proceed")

            # usecase selcteion
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecase",usecase_options)
            if self.user_controls["selected_usecase"] == "Chatbot with Web" or self.user_controls["selected_usecase"] == "AI News":
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"]=st.text_input("Tavily API key", type="password")
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠ Please enter your Tavily API key to proceed")
            
                elif self.user_controls["selected_usecase"] == "AI News":
                    st.subheader("AI News Explorer")
                    with st.sidebar:
                        time_frame = st.selectbox(
                            "📅 Select the time frame", 
                            ["Daily", "Weekly", "Monthly"], 
                            index=0)
                    if st.button("🔎 Fetch Latest AI News", use_container_width=True):
                        st.session_state.IsFetchButtonClicked = True
                        st.session_state.timeframe = time_frame
                    else:
                        st.session_state.IsFetchButtonClicked = False

        return self.user_controls
        

