# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Welcome",
        page_icon="👋",
    )

    st.write("# Trial Predict")

    #st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        
        TrialForecast is a groundbreaking open-source solution designed to enhance clinical trial 
        management. It aids clinicians in selecting optimal sites for clinical trials and 
        accurately predicting patient enrollment rates. 
        
        **Accelerating patient enrollment, reduce trial closures, and expediting the development of new therapies.**
        
        ### Want to learn more?
        - Something insightful
        - More text that is edgy with [documentation](https://docs.streamlit.io)
        - Ask a question in our to yourself
    """
    )


if __name__ == "__main__":
    run()
