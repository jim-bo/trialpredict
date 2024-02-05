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

from urllib.error import URLError

import altair as alt
import pandas as pd
from io import StringIO

import streamlit as st
from streamlit.hello.utils import show_code
#from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.tags import tagger_component

IMAGELU = {
    "Lung Cancer": "./assets/noun-lung-6507086.svg"
}

CANCER = {
    "Non-Small Cell Lung Cancer": ["Adenocarcinoma", "Squamous cell carcinoma", "Non-Squamous", "Large cell carcinoma"],
    "Small Cell Lung Cancer": ["SCLC-A", "SCLC-N", "SCLC-P", "SCLC-I"],
}

BURDEN = {
    "Non-Small Cell Lung Cancer": ["Local/Regional Primary", "Local/Regional Recurrence", "Metastatic"],
    "Small Cell Lung Cancer": ["Local/Regional Primary", "Local/Regional Recurrence", "Metastatic"]
}

MOLECULAR = {
    "Non-Small Cell Lung Cancer": {
        "Adenocarcinoma": ["EGFR-mutant", "KRAS-mutant", "ALK-positive", "ROS1-positive", " TP53-mutant", "STK11-mutant", "No targets"],
        "Squamous cell carcinoma": ["TP53-mutant", "CDKN2A-deleted", "PTEN-deficient", "EGFR-mutant", "No targets"],
        "Non-Squamous": ["EGFR-mutant", "KRAS-mutant", "ALK-positive", "ROS1-positive", " TP53-mutant", "STK11-mutant", "No targets"],
        "Large cell carcinoma": ["TP53-mutant", "No targets"]
    }, 
    "Small Cell Lung Cancer": {
        "SCLC-A": ["TP53", "RB1", "NOTCH1", "MYC AMP", "No targets"],
        "SCLC-N": ["TP53", "RB1", "NOTCH1", "MYC AMP", "No targets"],
        "SCLC-P": ["TP53", "RB1", "NOTCH1", "MYC AMP", "No targets"],
        "SCLC-I": ["TP53", "RB1", "NOTCH1", "MYC AMP", "No targets"]
    }
}

PRIOR = {
    "Non-Small Cell Lung Cancer": ["Platinum", "Platinum doublet", "Checkpoint",
     "ADCs", "Car-T"],
    "Small Cell Lung Cancer": ["Platinum", "Etopside", "Checkpoint"],
}

# bootstrap state
if "current_space" not in st.session_state:
    st.session_state["current_space"] = "Non-Small Cell Lung Cancer"
if "spaces" not in st.session_state:
    st.session_state['spaces'] = {
        "Non-Small Cell Lung Cancer": {
            "Cancer": ["Non-Small Cell Lung Cancer"],
            "Subtype": ["Adenocarinoma"],
            "Burden": ["Metastatic"],
            "Genomics": ["No targets"],
            "Prior therapy": ["Platinum doublet", "Pembrolizumab"]
        }
    }

# prepare the page
st.set_page_config(page_title="Trial criteria", page_icon="📊")

# title
st.markdown("# Clinical trial criteria")

# side back
st.sidebar.header("Trial criteria")

# introduction
st.markdown("""
Lets get started by entering in your clinical trail eligibility requirements. 

You can upload a file or select a trial from [clinicaltrials dot gov](https://clinicaltrials.gov/)
""")


tab1, tab2, tab3 = st.tabs(["Trial", "Refine", "Review"])

# trial eligibility
with tab1:
    # text area
    st.subheader("Trial eligibilty")
    st.write(("Please paste the relavent text from your clinical trial protocol which explains"
    "the inclusion and exclusion requirements of the trial"))

    txt = st.text_area(
        "Paste your eligibility criteria here",
    )

with tab2:
    st.subheader("Refine")
    st.markdown("""Please review the key clinical components we have extracted from your protocol known as trial
    *"clinical spaces"*. Where a clinical space is a combination of cancer type, subtype, disease status, treatment history and 
    disease burden. While other criteria are important the clinical space is the dominating factor in identifying relavent cohorts.\\
    \\
    You should review, edit or create any additional criteria as needed to ensure the trial forecasting is accurate.

    """)

    # simplify
    current_state = st.session_state["current_space"]
    space = st.session_state['spaces'][current_state]

    with st.container(border=True):
        cols = st.columns(3)
        with cols[0]:
            st.subheader("Non-Small Cell Lung Cancer")
        with cols[2]:
            st.image(IMAGELU["Lung Cancer"], width=50)
        st.divider()
        st.markdown("**Overview:** Metastatic lung adenocarcinoma with no targetable alterations and prior treatment with platinum doublet chemotherapy and single agent prembrolizumab")

        cols = st.columns(5)
        idx = 0
        with cols[idx]:
            tagger_component(
                "Cancer",
                space["Cancer"],
                color_name=["lightblue"] * len(space["Cancer"]),
            )
        idx += 1
        with cols[idx]:
            tagger_component(
                "Subtype",
                space["Subtype"],
                color_name=["green"] * len(space["Subtype"]),
            )
        idx += 1
        with cols[idx]:
            tagger_component(
                "Burden",
                space["Burden"],
                color_name=["red"] * len(space["Burden"]),
            )
        idx += 1
        with cols[idx]:
            tagger_component(
                "Genomics",
                space["Genomics"],
                color_name=["yellow"] * len(space["Genomics"]),
            )
        idx += 1
        with cols[idx]:
            tagger_component(
                "Prior therapy",
                space["Prior therapy"],
                color_name=["orange"] * len(space["Prior therapy"]),
            )
        idx += 1

        def update_space(key=None):
            """update value selected"""
            current_state = st.session_state["current_space"]
            st.session_state['spaces'][current_state][key] = [st.session_state[f"{key}/select"]]

        def update_multi_space(key=None):
            """update value selected"""
            current_state = st.session_state["current_space"]
            st.session_state['spaces'][current_state][key] = st.session_state[f"{key}/select"]

        with st.expander("Edit \"space\""):

            st.markdown("#### Cancer type")
            cancer_options = st.selectbox(
                'The cancer type according to the OncoTree Ontology',
                CANCER.keys(),
                key="Cancer/select",
                kwargs={"key": "Cancer"},
                on_change=update_space
            )

            st.markdown("#### Sub type")
            sub_option = st.selectbox(
                'The sub type of cancer according to the OncoTree Ontology',
                CANCER[cancer_options],
                key="Subtype/select",
                kwargs={"key": "Subtype"},
                on_change=update_space
            )

            st.markdown("#### Burden")
            option = st.selectbox(
                'Disease burden or treatment intent',
                BURDEN[cancer_options],
                key="Burden/select",
                kwargs={"key": "Burden"},
                on_change=update_space
            )

            st.markdown("#### Genomics")
            option = st.selectbox(
                'Genomic alterations',
                MOLECULAR[cancer_options][sub_option],
                key="Genomics/select",
                kwargs={"key": "Genomics"},
                on_change=update_space
            )

            st.markdown("#### Prior therapy")
            option = st.multiselect(
                'Therapies the patient must have also had',
                PRIOR[cancer_options],
                default=space['Prior therapy'] if space['Prior therapy'] in PRIOR[cancer_options] else None,
                key="Prior therapy/select",
                kwargs={"key": "Prior therapy"},
                on_change=update_multi_space
            )