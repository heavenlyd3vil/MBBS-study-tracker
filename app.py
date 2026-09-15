import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import json
import copy
import math

st.set_page_config(
    page_title="Medical Study Tracker",
    page_icon="📚",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F4FAF5;
    }

    [data-testid="stSidebar"] {
        background-color: #E5F2E7;
    }

    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }

    .stButton {
        margin: 0 !important;
        padding: 0 !important;
    }

    .stButton > button {
        border-radius: 10px !important;
        border: 2px solid #A8CDB0 !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }

    .stButton > button p,
    .stButton > button span {
        color: #000000 !important;
    }

    .stButton > button:hover {
        border-color: #76B889 !important;
        background-color: #EEF8F0 !important;
        color: #000000 !important;
    }

    .stButton > button[kind="primary"] {
        background-color: #8FC9A3 !important;
        border: 2px solid #5FAF78 !important;
        color: #000000 !important;
    }

    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span {
        color: #000000 !important;
    }

    /* ========================================================
       SUBJECT CARDS
       ======================================================== */

    [class*="st-key-subject_card_"] {
        border: 2px solid #A8CDB0 !important;
        border-radius: 14px !important;
        background-color: #FFFFFF !important;
        padding: 14px !important;
        margin: 0 !important;
    }

    [class*="st-key-subject_card_"] [data-testid="stVerticalBlock"] {
        gap: 0.25rem !important;
    }

    [class*="st-key-subject_card_"] [data-testid="element-container"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    [class*="st-key-subject_card_"] .stButton > button {
        height: 52px !important;
        min-height: 52px !important;
        padding: 4px 10px !important;
        border-radius: 10px !important;
        font-size: 16px !important;
    }

    /* ========================================================
       TOPIC CARDS
       ======================================================== */

    [class*="st-key-topic_card_"] {
        border: 2px solid #A8CDB0 !important;
        border-radius: 14px !important;
        background-color: #FFFFFF !important;
        padding: 14px !important;
        margin: 0 !important;
    }

    [class*="st-key-topic_card_"] [data-testid="stVerticalBlock"] {
        gap: 0.25rem !important;
    }

    [class*="st-key-topic_card_"] [data-testid="element-container"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    [class*="st-key-topic_card_"] .stButton > button {
        height: 50px !important;
        min-height: 50px !important;
        padding: 4px 8px !important;
        border-radius: 10px !important;
        font-size: 15px !important;
    }

    [class*="st-key-subject_card_"] [data-testid="stMarkdown"],
    [class*="st-key-topic_card_"] [data-testid="stMarkdown"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    [class*="st-key-subject_card_"] [data-testid="stMarkdownContainer"],
    [class*="st-key-topic_card_"] [data-testid="stMarkdownContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    [class*="st-key-topic_card_"] [data-testid="stHorizontalBlock"] {
        gap: 0.4rem !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    [class*="st-key-topic_card_"] [data-testid="stColumn"] {
        padding: 0 !important;
    }

    /* ========================================================
       DETAIL CARD
       ======================================================== */

    [class*="st-key-topic_detail_"] {
        border: 2px solid #A8CDB0 !important;
        border-radius: 14px !important;
        background-color: #FFFFFF !important;
        padding: 20px !important;
        gap: 0 !important;
    }

    [class*="st-key-topic_detail_"] [data-testid="stVerticalBlock"] {
        gap: 0.25rem !important;
    }

    [class*="st-key-topic_detail_"] [data-testid="stMarkdown"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    [class*="st-key-topic_detail_"] [data-testid="stMarkdownContainer"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    [class*="st-key-topic_detail_"] hr {
        border: none !important;
        border-top: 1px solid #C8E0CC !important;
        margin-top: 7px !important;
        margin-bottom: 7px !important;
    }

    /* ========================================================
       CHECKBOXES
       ======================================================== */

    [data-testid="stCheckbox"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stCheckbox"] label {
        color: #000000 !important;
    }

    [data-testid="stCheckbox"] label span {
        color: #000000 !important;
    }

    [data-testid="stHorizontalBlock"] {
        gap: 0.6rem !important;
    }

    hr {
        border-color: #C8E0CC !important;
    }

    /* ========================================================
       RESET BUTTON
       ======================================================== */

    [data-testid="stSidebar"] .reset-button button {
        border: 2px solid #D99A9A !important;
        background-color: #F3CACA !important;
        color: #000000 !important;
    }

    [data-testid="stSidebar"] .reset-button button:hover {
        border-color: #C77777 !important;
        background-color: #EFB7B7 !important;
        color: #000000 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DEFAULT SYLLABUS
# ============================================================

DEFAULT_YEARS = {
    "First Year": {
        "Anatomy": {
            "General Anatomy": {},
            "Embryology": {},
            "Histology": {},
            "Neuroanatomy": {},
            "Head and Neck": {},
            "Upper Limb": {},
            "Lower Limb": {},
            "Thorax": {},
            "Abdomen": {}
        },
        "Physiology": {
            "General": {},
            "Nerve Muscle": {},
            "CNS": {},
            "CVS": {},
            "Respiratory": {},
            "Renal": {},
            "Gastro": {},
            "Endocrine": {},
            "Reproductive and Exercise": {}
        },
        "Biochemistry": {
            "General": {},
            "Enzyme": {},
            "Carbohydrate": {},
            "Lipid": {},
            "Protein": {},
            "Molecular Biology": {},
            "Vitamins": {},
            "Miscellaneous": {}
        }
    },

    "Second Year": {
        "Pathology": {
            "General": {},
            "Hematology": {},
            "CNS": {},
            "CVS": {},
            "Respiratory": {},
            "Genitourinary": {},
            "Skin and Musculoskeletal": {},
            "Endocrine": {},
            "Gastrointestinal": {}
        },
        "Pharmacology": {
            "General": {},
            "ANS": {},
            "CVS": {},
            "Renal": {},
            "CNS": {},
            "Endocrine": {},
            "Respiratory": {},
            "GI": {},
            "Hematology": {},
            "Antimicrobial": {},
            "Autocoids": {},
            "Immunomodulator and Anti Cancer": {}
        },
        "Microbiology": {
            "General": {},
            "Bacteria": {},
            "Virus": {},
            "Fungi": {},
            "Parasites": {},
            "Immunology": {}
        }
    },

    "Third Year": {
        "FMT": {
            "Traumatology": {},
            "Ballistics": {},
            "Medical Jurisprudence": {},
            "Autopsy": {},
            "Human Identification": {},
            "Asphyxia": {},
            "Sexual Jurisprudence": {},
            "Toxicology": {},
            "Forensic Psychiatry": {}
        },
        "PSM": {
            "Demography And Family Planning": {},
            "MCH": {},
            "Immunisation": {},
            "National Health Programs": {},
            "Epidemiology": {},
            "Screening": {},
            "Biostatistics": {},
            "Healthcare Planning": {},
            "Infectious": {},
            "Communicable": {},
            "Non Communicable": {},
            "Nutrition": {},
            "Environment": {},
            "BMW": {},
            "Occupational Health": {},
            "Concept of Health": {},
            "Health Communication": {},
            "International Health Organisation": {},
            "Social Medicine": {},
            "Miscellaneous": {},
            "Recent Updates": {}
        },
        "Ophthalmology": {
            "Basics": {},
            "Cornea Sclera": {},
            "Neuro Ophthalmology": {},
            "Squint": {},
            "Lens and Blunt Trauma": {},
            "Uvea": {},
            "Glaucoma": {},
            "Optics": {},
            "Retina": {},
            "Eyelids Orbit": {},
            "Conjunctiva": {}
        },
        "ENT": {
            "Ear": {},
            "Nose": {},
            "Pharynx": {},
            "Larynx": {}
        }
    },

    "Major": {
        "Medicine": {
            "Gastroenterology": {}, "Endocrine": {}, "Hematology": {},
            "Respiratory": {}, "Nephrology": {}, "Hepatology": {},
            "Cardiology": {}, "ECG": {}, "Neurology": {},
            "Rheumatology": {}, "Acid base": {}, "Infectious": {}
        },
        "Surgery": {
            "General": {}, "Breast": {}, "Endocrine": {}, "Abdominal": {},
            "Urology": {}, "Specialty": {}, "Trauma": {}, "Hernia": {},
            "Vascular": {}, "Faciomaxillary": {}, "Miscellaneous": {}
        },
        "OBG": {
            "General gynae": {}, "Gynae infections": {}, "Infertility": {},
            "Contraception": {}, "Oncology": {},
            "Fundamentals of reproduction": {}, "Normal pregnancy and ANC": {},
            "Medical and surgical complications": {}, "Obstetric complications": {},
            "Labor and puerperium": {}
        },
        "Paediatrics": {
            "Neonatology": {}, "Growth and development": {}, "Nutrition": {},
            "Genetic disorders": {}, "Childhood infections": {},
            "Gastrointestinal": {}, "Respiratory": {}, "Genitourinary": {},
            "Cardiovascular": {}, "Nervous": {}, "Endocrine": {},
            "Rheumatology": {}, "Malignancies": {}, "Hematology": {},
            "Miscellaneous": {}
        }
    },

    "Minor": {
        "Orthopaedics": {},
        "Dermatology": {},
        "Psychiatry": {},
        "Radiology": {},
        "Anaesthesia": {}
    }
}


# ============================================================
# DATABASE
# ============================================================
#
# Local SQLite is used for instant UI saves.
# Supabase is used as the persistent cloud backup.
# Cloud uploads happen in the background so button clicks do not
# wait for the network.
# ============================================================

DB_FILE = "medical_tracker.db"

from concurrent.futures import ThreadPoolExecutor
from supabase import create_client


@st.cache_resource
def get_supabase_client():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )


@st.cache_resource
def get_sync_executor():
    return ThreadPoolExecutor(max_workers=1)


def create_local_database():

    connection = sqlite3.connect(DB_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tracker_data (
            id INTEGER PRIMARY KEY,
            data TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def load_local_database():

    create_local_database()

    connection = sqlite3.connect(DB_FILE)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT data FROM tracker_data WHERE id = 1"
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    try:
        return json.loads(result[0])
    except Exception:
        return None


def save_local_database(data):

    create_local_database()

    connection = sqlite3.connect(DB_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO tracker_data (id, data)
        VALUES (1, ?)
        """,
        (json.dumps(data),)
    )

    connection.commit()
    connection.close()


def cloud_save(data):

    try:
        client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

        (
            client
            .table("tracker_data")
            .upsert(
                {
                    "id": 1,
                    "data": data
                }
            )
            .execute()
        )

    except Exception:
        # The local SQLite copy has already been saved.
        # Cloud syncing will be attempted again on the next save.
        pass


def load_database():

    try:
        client = get_supabase_client()

        result = (
            client
            .table("tracker_data")
            .select("data")
            .eq("id", 1)
            .execute()
        )

        if result.data:
            cloud_data = result.data[0]["data"]

            # Keep a local copy as well.
            save_local_database(cloud_data)

            return cloud_data

    except Exception:
        pass

    # If Supabase is temporarily unavailable or has no data,
    # use the local copy.
    return load_local_database()


def save_database(data):

    # 1. Save locally first. This is effectively instantaneous.
    save_local_database(data)

    # 2. Send a snapshot to Supabase in the background.
    data_snapshot = copy.deepcopy(data)

    get_sync_executor().submit(
        cloud_save,
        data_snapshot
    )

# ============================================================
# LOAD DATA
# ============================================================

if "years" not in st.session_state:

    saved_data = load_database()

    if saved_data is not None:

        st.session_state.years = saved_data

    else:

        st.session_state.years = copy.deepcopy(
            DEFAULT_YEARS
        )

        save_database(
            st.session_state.years
        )


years = st.session_state.years


# ============================================================
# CLEAN DATA
# ============================================================

def clean_normal_year(year_data):

    if not isinstance(year_data, dict):
        return {}

    cleaned_year = {}

    for subject_name, topics in year_data.items():

        if not isinstance(topics, dict):
            topics = {}

        cleaned_topics = {}

        for topic_name, topic_data in topics.items():

            if topic_name in {
                "subject_pyqs",
                "subject_test"
            }:
                cleaned_topics[topic_name] = bool(topic_data)

            elif isinstance(topic_data, dict):
                cleaned_topics[topic_name] = topic_data

            else:
                cleaned_topics[topic_name] = {}

        cleaned_year[subject_name] = cleaned_topics

    return cleaned_year


for year_name in [
    "First Year",
    "Second Year",
    "Third Year"
]:

    years[year_name] = clean_normal_year(
        years.get(year_name, {})
    )


for page_name in [
    "Major"
]:

    years[page_name] = clean_normal_year(
        years.get(page_name, {})
    )


# ============================================================
# CLEAN OLD MAJOR STRUCTURE
# ============================================================
# Major used to contain tracker components such as:
# notes, revision, question_banks, pyqs and subject_test
# directly as topics. Major now follows the same structure as
# Years 1-3: Medicine/Surgery/OBG/Paediatrics each contain
# their actual syllabus subtopics. Remove any old component
# entries while preserving progress for valid subtopics.
# ============================================================

if isinstance(years.get("Major"), dict):
    cleaned_major = {}

    for subject_name, default_topics in DEFAULT_YEARS.get("Major", {}).items():
        existing_topics = years["Major"].get(subject_name, {})

        if not isinstance(existing_topics, dict):
            existing_topics = {}

        cleaned_major[subject_name] = {}

        # Preserve subject-level tracking fields.
        cleaned_major[subject_name]["subject_pyqs"] = existing_topics.get(
            "subject_pyqs", False
        )
        cleaned_major[subject_name]["subject_test"] = existing_topics.get(
            "subject_test", False
        )

        for topic_name in default_topics:
            if topic_name in existing_topics and isinstance(existing_topics[topic_name], dict):
                cleaned_major[subject_name][topic_name] = existing_topics[topic_name]
            else:
                cleaned_major[subject_name][topic_name] = {}

    years["Major"] = cleaned_major


# ============================================================
# ADD MISSING SYLLABUS ITEMS
# ============================================================

for year_name, default_year in DEFAULT_YEARS.items():

    if year_name not in years:

        years[year_name] = copy.deepcopy(
            default_year
        )

    for subject_name, topics in default_year.items():

        if subject_name not in years[year_name]:

            years[year_name][subject_name] = copy.deepcopy(
                topics
            )

        elif not isinstance(
            years[year_name][subject_name],
            dict
        ):

            years[year_name][subject_name] = copy.deepcopy(
                topics
            )

        else:

            for topic_name in topics:

                if topic_name not in years[
                    year_name
                ][subject_name]:

                    years[
                        year_name
                    ][subject_name][topic_name] = {}


# ============================================================
# ADD SUBJECT-LEVEL PYQ / TEST TRACKING
# ============================================================
# These two fields belong to the subject itself, not to an
# individual topic. They are used for the subject-level
# checkboxes and the green/red status boxes on the Year pages.
# ============================================================

for year_name in [
    "First Year",
    "Second Year",
    "Third Year",
    "Major"
]:

    for subject_name in years.get(year_name, {}):

        subject_data = years[year_name][subject_name]

        if not isinstance(subject_data, dict):
            subject_data = {}
            years[year_name][subject_name] = subject_data

        subject_data.setdefault("subject_pyqs", False)
        subject_data.setdefault("subject_test", False)

save_database(years)


# ============================================================
# NAVIGATION STATE
# ============================================================

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "home"

if "selected_year" not in st.session_state:
    st.session_state.selected_year = None

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

if "show_reset_confirmation" not in st.session_state:
    st.session_state.show_reset_confirmation = False


# ============================================================
# NAVIGATION FUNCTIONS
# ============================================================

def go_home():

    st.session_state.selected_page = "home"
    st.session_state.selected_year = None
    st.session_state.selected_subject = None
    st.session_state.selected_topic = None


def go_year(year):

    st.session_state.selected_page = "year"
    st.session_state.selected_year = year
    st.session_state.selected_subject = None
    st.session_state.selected_topic = None


def go_subject(year, subject):

    st.session_state.selected_page = "subject"
    st.session_state.selected_year = year
    st.session_state.selected_subject = subject
    st.session_state.selected_topic = None


def go_topic(year, subject, topic):

    st.session_state.selected_page = "topic"
    st.session_state.selected_year = year
    st.session_state.selected_subject = subject
    st.session_state.selected_topic = topic


# ============================================================
# HELPERS
# ============================================================

def css_key(text):

    return (
        str(text)
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )


def _safe_number(value):

    if isinstance(value, bool):
        return 0

    if isinstance(value, (int, float)):
        return max(0, min(100, value))

    return 0


def _safe_bool(value):

    return value is True


def _real_topics(data):

    if not isinstance(data, dict):
        return []

    return [
        topic_data
        for topic_name, topic_data in data.items()
        if topic_name not in {
            "subject_pyqs",
            "subject_test"
        }
        and isinstance(topic_data, dict)
    ]


def get_topic_percentage(topic_data):

    if not isinstance(topic_data, dict):
        return 0

    # Displayed topic progress: Notes, Revision Notes and
    # Question Banks only. Topic PYQs are tracked separately.
    return (
        _safe_number(topic_data.get("notes", 0))
        + _safe_number(topic_data.get("revision", 0))
        + _safe_number(topic_data.get("question_banks", 0))
    ) / 3


def get_topic_academic_percentage(topic_data):

    if not isinstance(topic_data, dict):
        return 0

    # The four topic-level components are kept separate and
    # contribute equally inside the 85% topic component:
    # Notes, Revision Notes, Question Banks and Topic PYQs.
    topic_pyqs = 100 if _safe_bool(topic_data.get("pyqs", False)) else 0

    return (
        _safe_number(topic_data.get("notes", 0))
        + _safe_number(topic_data.get("revision", 0))
        + _safe_number(topic_data.get("question_banks", 0))
        + topic_pyqs
    ) / 4


def get_subtopic_full_score(topic_data):

    if not isinstance(topic_data, dict):
        return 0

    # Minor has no subtopics. Each Minor entry is itself a
    # complete subject, so its Notes/Revision/Question Banks
    # make up 85%, its PYQs 10% and its Test 5%.
    study_progress = (
        _safe_number(topic_data.get("notes", 0))
        + _safe_number(topic_data.get("revision", 0))
        + _safe_number(topic_data.get("question_banks", 0))
    ) / 3

    pyqs = 100 if _safe_bool(topic_data.get("pyqs", False)) else 0
    test = 100 if _safe_bool(topic_data.get("subject_test", False)) else 0

    return (
        study_progress * 0.85
        + pyqs * 0.10
        + test * 0.05
    )


def get_subtopic_academic_score(topic_data):

    if not isinstance(topic_data, dict):
        return 0

    return get_topic_academic_percentage(topic_data)


def get_subject_topic_progress(topics):

    real_topics = _real_topics(topics)

    if not real_topics:
        return 0

    scores = [
        get_topic_percentage(topic_data)
        for topic_data in real_topics
    ]

    return sum(scores) / len(scores)


def get_subject_topic_progress_academic(subject_data):

    real_topics = _real_topics(subject_data)

    if not real_topics:
        return 0

    scores = [
        get_topic_academic_percentage(topic_data)
        for topic_data in real_topics
    ]

    return sum(scores) / len(scores)


def get_subject_overall_progress(subject_data):

    if not isinstance(subject_data, dict):
        return 0

    real_topics = _real_topics(subject_data)

    # 85% = actual topic work, with Notes, Revision Notes,
    # Question Banks and Topic PYQs each accounted for separately.
    if real_topics:
        topic_component = (
            sum(
                get_topic_academic_percentage(topic_data)
                for topic_data in real_topics
            ) / len(real_topics)
        )
    else:
        topic_component = 0

    # The remaining 15% belongs to the subject as a whole:
    # Subject PYQs = 10%, Subject Test = 5%.
    subject_pyq = 100 if _safe_bool(subject_data.get("subject_pyqs", False)) else 0
    subject_test = 100 if _safe_bool(subject_data.get("subject_test", False)) else 0

    return (
        topic_component * 0.85
        + subject_pyq * 0.10
        + subject_test * 0.05
    )


def get_subject_academic_progress(topics):

    real_topics = _real_topics(topics)

    if not real_topics:
        return 0

    scores = [
        get_topic_academic_percentage(topic_data)
        for topic_data in real_topics
    ]

    return sum(scores) / len(scores)


def get_pyq_progress(topics):

    if not isinstance(topics, dict):
        return 0, "0/0"

    valid_topics = _real_topics(topics)

    if not valid_topics:
        return 0, "0/0"

    completed = sum(
        1
        for topic_data in valid_topics
        if _safe_bool(topic_data.get("pyqs", False))
    )

    total = len(valid_topics)
    percentage = (completed / total) * 100

    return percentage, f"{completed}/{total}"


def get_test_progress(topics):

    if not isinstance(topics, dict):
        return 0, "0/0"

    valid_topics = _real_topics(topics)

    if not valid_topics:
        return 0, "0/0"

    completed = sum(
        1
        for topic_data in valid_topics
        if _safe_bool(topic_data.get("subject_test", False))
    )

    total = len(valid_topics)
    percentage = (completed / total) * 100

    return percentage, f"{completed}/{total}"


def get_year_progress(year):

    # Minor has no subtopics. Each Minor entry is itself a
    # complete subject, so calculate each entry directly.
    if year == "Minor":
        topic_scores = []
        for topic_data in years.get("Minor", {}).values():
            if isinstance(topic_data, dict):
                topic_scores.append(get_subtopic_full_score(topic_data))

        if not topic_scores:
            return 0

        # Minor is separate from the 9-semester overall weighting.
        return sum(topic_scores) / len(topic_scores)

    year_data = years.get(year, {})

    # No subject-wise weighting for the 85% topic component:
    # every actual topic in the year counts equally.
    all_topic_scores = []
    subject_pyq_scores = []
    subject_test_scores = []

    for subject_data in year_data.values():
        if not isinstance(subject_data, dict):
            continue

        real_topics = _real_topics(subject_data)
        if not real_topics:
            continue

        all_topic_scores.extend(
            get_topic_academic_percentage(topic_data)
            for topic_data in real_topics
        )

        # These are subject-level items and are therefore counted
        # once for the subject as a whole, not once per topic.
        subject_pyq_scores.append(
            100 if _safe_bool(subject_data.get("subject_pyqs", False)) else 0
        )
        subject_test_scores.append(
            100 if _safe_bool(subject_data.get("subject_test", False)) else 0
        )

    if not all_topic_scores:
        return 0

    topic_component = sum(all_topic_scores) / len(all_topic_scores)
    subject_pyq_component = (
        sum(subject_pyq_scores) / len(subject_pyq_scores)
        if subject_pyq_scores else 0
    )
    subject_test_component = (
        sum(subject_test_scores) / len(subject_test_scores)
        if subject_test_scores else 0
    )

    return (
        topic_component * 0.85
        + subject_pyq_component * 0.10
        + subject_test_component * 0.05
    )


def get_overall_progress():

    # Curriculum time weighting from the 9-semester structure:
    # First Year = 2 semesters, Second Year = 2,
    # Third Year = 3, Major = 2.
    # Minor is completely separate from this calculation.
    semester_weights = {
        "First Year": 2,
        "Second Year": 2,
        "Third Year": 3,
        "Major": 2
    }

    total_weighted_progress = 0
    total_weight = 0

    for year_name, semester_weight in semester_weights.items():
        year_progress = get_year_progress(year_name)

        # A year represents its number of semesters, regardless of
        # how many subjects or topics happen to be inside it.
        total_weighted_progress += year_progress * semester_weight
        total_weight += semester_weight

    if total_weight == 0:
        return 0

    return total_weighted_progress / total_weight


def get_progress_color(percentage):

    percentage = max(
        0,
        min(100, percentage)
    )

    start_r, start_g, start_b = 185, 220, 192
    end_r, end_g, end_b = 91, 169, 116

    ratio = percentage / 100

    r = int(
        start_r
        + (end_r - start_r) * ratio
    )

    g = int(
        start_g
        + (end_g - start_g) * ratio
    )

    b = int(
        start_b
        + (end_b - start_b) * ratio
    )

    return f"rgb({r}, {g}, {b})"


def progress_bar(
    percentage,
    label
):

    percentage = max(
        0,
        min(100, percentage)
    )

    fill_color = get_progress_color(
        percentage
    )

    st.markdown(
        f"""<div style="
            width: 100%;
            height: 30px;
            border-radius: 9px;
            background: linear-gradient(
                to right,
                {fill_color} {percentage:.2f}%,
                #E5F2E7 {percentage:.2f}%
            );
            border: 1px solid #A8CDB0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #000000;
            font-weight: bold;
            font-size: 13px;
            margin: 0;
            padding: 0;
        ">{label}</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# STATUS BOX
# ============================================================

def status_box(
    label,
    completed
):

    if completed:

        background_color = "#8FC9A3"
        border_color = "#5FAF78"

    else:

        background_color = "#F3CACA"
        border_color = "#D99A9A"

    st.markdown(
        f"""<div style="
            width: 100%;
            height: 36px;
            box-sizing: border-box;
            border: 2px solid {border_color};
            border-radius: 8px;
            padding: 0 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #000000;
            background-color: {background_color};
            font-weight: 600;
            font-size: 14px;
            line-height: 1;
            margin: 0;
        ">{label}</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# CONTINUOUS SVG PIZZA
# ============================================================

def draw_pizza(percentage):

    percentage = max(
        0,
        min(100, percentage)
    )

    cx = 200
    cy = 200
    radius = 130

    eaten_angle = percentage * 3.6

    # --------------------------------------------------------
    # Eaten section
    # --------------------------------------------------------

    if percentage <= 0:

        eaten_path = ""

    elif percentage >= 100:

        eaten_path = f"""
        <circle
            cx="{cx}"
            cy="{cy}"
            r="145"
            fill="#F4FAF5"
        />
        """

    else:

        start_angle = -90
        end_angle = (
            start_angle
            + eaten_angle
        )

        start_rad = math.radians(
            start_angle
        )

        end_rad = math.radians(
            end_angle
        )

        start_x = (
            cx
            + radius
            * math.cos(start_rad)
        )

        start_y = (
            cy
            + radius
            * math.sin(start_rad)
        )

        end_x = (
            cx
            + radius
            * math.cos(end_rad)
        )

        end_y = (
            cy
            + radius
            * math.sin(end_rad)
        )

        large_arc = (
            1
            if eaten_angle > 180
            else 0
        )

        eaten_path = f"""
        <path
            d="
                M {cx} {cy}
                L {start_x:.3f} {start_y:.3f}
                A {radius} {radius}
                0 {large_arc} 1
                {end_x:.3f} {end_y:.3f}
                Z
            "
            fill="#F4FAF5"
        />
        """

    # --------------------------------------------------------
    # Pepperoni
    # --------------------------------------------------------

    pepperoni = [
        (135, 145),
        (250, 140),
        (185, 210),
        (265, 245),
        (135, 255),
        (205, 285),
        (215, 125)
    ]

    pepperoni_svg = ""

    for x, y in pepperoni:

        pepperoni_svg += f"""
        <circle
            cx="{x}"
            cy="{y}"
            r="13"
            fill="#C94D45"
            stroke="#A83D38"
            stroke-width="2"
        />
        """

    # --------------------------------------------------------
    # Cheese highlights
    # --------------------------------------------------------

    cheese_spots = [
        (125, 200),
        (270, 190),
        (175, 265),
        (235, 215),
        (165, 135)
    ]

    cheese_svg = ""

    for x, y in cheese_spots:

        cheese_svg += f"""
        <circle
            cx="{x}"
            cy="{y}"
            r="7"
            fill="#FFF1A8"
        />
        """

    # --------------------------------------------------------
    # SVG document
    # --------------------------------------------------------

    svg = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <style>

            html, body {{
                margin: 0;
                padding: 0;
                background: transparent;
                overflow: hidden;
            }}

            .pizza-container {{
                width: 100%;
                height: 350px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            svg {{
                display: block;
            }}

        </style>

    </head>

    <body>

        <div class="pizza-container">

            <svg
                width="340"
                height="340"
                viewBox="0 0 400 400"
                xmlns="http://www.w3.org/2000/svg"
            >

                <!-- Plate -->

                <circle
                    cx="200"
                    cy="200"
                    r="166"
                    fill="#FFFFFF"
                    stroke="#C8E0CC"
                    stroke-width="3"
                />

                <!-- Pizza crust -->

                <circle
                    cx="200"
                    cy="200"
                    r="148"
                    fill="#D49A52"
                    stroke="#B97E42"
                    stroke-width="5"
                />

                <!-- Tomato sauce -->

                <circle
                    cx="200"
                    cy="200"
                    r="139"
                    fill="#E76F51"
                />

                <!-- Cheese -->

                <circle
                    cx="200"
                    cy="200"
                    r="130"
                    fill="#F4D06F"
                    stroke="#E5B84B"
                    stroke-width="2"
                />

                <!-- Pepperoni -->

                {pepperoni_svg}

                <!-- Cheese highlights -->

                {cheese_svg}

                <!-- Eaten portion -->

                {eaten_path}

            </svg>

        </div>

    </body>

    </html>
    """

    components.html(
        svg,
        height=350,
        scrolling=False
    )


# ============================================================
# PROGRESS BUTTONS
# ============================================================

def progress_buttons(
    topic_data,
    year,
    subject,
    topic,
    label,
    key_name
):

    st.markdown(
        f"""
        <div style="
            color: #000000;
            font-weight: 600;
            font-size: 15px;
            margin: 0 0 2px 0;
            padding: 0;
        ">
            {label}
        </div>
        """,
        unsafe_allow_html=True
    )

    values = [
        0,
        25,
        50,
        75,
        100
    ]

    columns = st.columns(
        5,
        gap="small"
    )

    current_value = topic_data.get(
        key_name,
        0
    )

    for i, value in enumerate(values):

        with columns[i]:

            if st.button(
                f"{value}%",
                key=(
                    f"progress_"
                    f"{css_key(year)}_"
                    f"{css_key(subject)}_"
                    f"{css_key(topic)}_"
                    f"{key_name}_"
                    f"{value}"
                ),
                use_container_width=True,
                type=(
                    "primary"
                    if current_value == value
                    else "secondary"
                )
            ):

                topic_data[key_name] = value

                save_database(
                    st.session_state.years
                )

                st.rerun()


# ============================================================
# TOPIC DETAIL
# ============================================================

def show_topic_detail(
    year,
    subject,
    topic
):

    topic_data = years[
        year
    ][
        subject
    ][
        topic
    ]

    if st.button(
        f"← Back to {subject}",
        key=(
            f"topic_back_"
            f"{css_key(year)}_"
            f"{css_key(subject)}_"
            f"{css_key(topic)}"
        )
    ):

        go_subject(
            year,
            subject
        )

        st.rerun()

    st.title(topic)

    percentage = get_topic_academic_percentage(
        topic_data
    )

    progress_bar(
        percentage,
        f"{percentage:.1f}%"
    )

    st.markdown(
        "<div style='height: 10px;'></div>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        "<div style='height: 6px;'></div>",
        unsafe_allow_html=True
    )

    progress_buttons(
        topic_data,
        year,
        subject,
        topic,
        "Notes",
        "notes"
    )

    st.divider()

    progress_buttons(
        topic_data,
        year,
        subject,
        topic,
        "Revision Notes",
        "revision"
    )

    st.divider()

    progress_buttons(
        topic_data,
        year,
        subject,
        topic,
        "Question Banks",
        "question_banks"
    )

    st.divider()

    pyq = st.checkbox(
        "Topic Pyqs",
        value=topic_data.get(
            "pyqs",
            False
        ),
        key=(
            f"detail_pyq_"
            f"{css_key(year)}_"
            f"{css_key(subject)}_"
            f"{css_key(topic)}"
        )
    )

    old_pyq = topic_data.get("pyqs", False)

    if pyq != old_pyq:
        topic_data["pyqs"] = pyq
        save_database(
            st.session_state.years
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "📚 Medical Study Tracker"
)

st.sidebar.divider()


if st.sidebar.button(
    "🏠 Home",
    use_container_width=True
):

    go_home()

    st.rerun()


st.sidebar.divider()


for page_name in [
    "First Year",
    "Second Year",
    "Third Year",
    "Major",
    "Minor"
]:

    if st.sidebar.button(
        page_name,
        key=f"sidebar_{css_key(page_name)}",
        use_container_width=True
    ):

        go_year(page_name)

        st.rerun()


# ============================================================
# RESET BUTTON
# ============================================================

st.sidebar.divider()


st.sidebar.markdown(
    '<div class="reset-button">',
    unsafe_allow_html=True
)


if st.sidebar.button(
    "Reset All Progress",
    use_container_width=True,
    key="reset_all_progress"
):

    st.session_state.show_reset_confirmation = True


st.sidebar.markdown(
    "</div>",
    unsafe_allow_html=True
)


if st.session_state.show_reset_confirmation:

    st.sidebar.warning(
        "This will erase ALL saved progress."
    )

    confirm_col1, confirm_col2 = st.sidebar.columns(
        2,
        gap="small"
    )

    with confirm_col1:

        if st.button(
            "Cancel",
            key="cancel_reset",
            use_container_width=True
        ):

            st.session_state.show_reset_confirmation = False

            st.rerun()

    with confirm_col2:

        if st.button(
            "RESET",
            key="confirm_reset",
            use_container_width=True
        ):

            st.session_state.years = copy.deepcopy(
                DEFAULT_YEARS
            )

            save_database(
                st.session_state.years
            )

            st.session_state.show_reset_confirmation = False

            go_home()

            st.rerun()


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.selected_page == "home":

    overall_progress = get_overall_progress()

    draw_pizza(
        overall_progress
    )

    st.markdown(
        f"""
        <div style="
            text-align: center;
            color: #000000;
            font-size: 32px;
            font-weight: 800;
            margin-top: -10px;
        ">
            {overall_progress:.1f}%
        </div>

        <div style="
            text-align: center;
            color: #000000;
            font-size: 15px;
            font-weight: 600;
            margin-top: 2px;
        ">
            of the syllabus consumed
        </div>

        <div style="
            text-align: center;
            color: #555555;
            font-size: 13px;
            margin-top: 7px;
            margin-bottom: 10px;
        ">
            Keep eating.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# YEAR PAGE
# ============================================================

elif st.session_state.selected_page == "year":

    year = st.session_state.selected_year

    # ========================================================
    # MAJOR
    # ========================================================

    if year == "Major":

        st.title(year)

        year_progress = get_year_progress(
            year
        )

        progress_bar(
            year_progress,
            f"Year Progress {year_progress:.1f}%"
        )

        st.divider()

        subjects = years[year]

        columns = st.columns(
            3,
            gap="small"
        )

        for i, subject in enumerate(subjects):

            topics = subjects[subject]

            subject_progress = get_subject_overall_progress(
                topics
            )

            with columns[i % 3]:

                with st.container(
                    border=True,
                    key=(
                        "subject_card_"
                        f"{css_key(year)}_"
                        f"{css_key(subject)}"
                    ),
                    gap="small"
                ):

                    if st.button(
                        subject,
                        key=(
                            f"subject_"
                            f"{css_key(year)}_"
                            f"{css_key(subject)}"
                        ),
                        use_container_width=True
                    ):

                        go_subject(
                            year,
                            subject
                        )

                        st.rerun()

                    progress_bar(
                        subject_progress,
                        f"{subject_progress:.1f}%"
                    )

                    subject_pyq_status = topics.get(
                        "subject_pyqs", False
                    )
                    subject_test_status = topics.get(
                        "subject_test", False
                    )

                    status_col1, status_col2 = st.columns(
                        2,
                        gap="small"
                    )
                    with status_col1:
                        status_box(
                            "Subject PYQs",
                            subject_pyq_status
                        )
                    with status_col2:
                        status_box(
                            "Subject Test",
                            subject_test_status
                        )

    # ========================================================
    # MINOR (DIRECT TOPICS)
    # ========================================================

    elif year == "Minor":

        page_data = years[year]
        st.title(year)

        topic_percentage = get_year_progress("Minor")
        progress_bar(topic_percentage, f"Minor Progress {topic_percentage:.1f}%")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        pyq_percentage, pyq_fraction = get_pyq_progress(page_data)
        test_percentage, test_fraction = get_test_progress(page_data)

        col1, col2 = st.columns(2, gap="small")
        with col1:
            progress_bar(pyq_percentage, f"PYQs {pyq_fraction}")
        with col2:
            progress_bar(test_percentage, f"Tests {test_fraction}")

        st.divider()
        st.subheader("Topics")
        columns = st.columns(3, gap="small")

        for i, topic in enumerate(page_data):
            topic_data = page_data[topic]
            if not isinstance(topic_data, dict):
                topic_data = {}
                page_data[topic] = topic_data

            topic_percentage = get_topic_percentage(topic_data)
            pyq_status = topic_data.get("pyqs", False) is True
            test_status = topic_data.get("subject_test", False) is True

            with columns[i % 3]:
                with st.container(
                    border=True,
                    key=f"topic_card_{css_key(year)}_{css_key(topic)}",
                    gap="small"
                ):
                    if st.button(
                        topic,
                        key=f"major_minor_topic_{css_key(year)}_{css_key(topic)}",
                        use_container_width=True
                    ):
                        go_subject(year, topic)
                        st.rerun()

                    progress_bar(topic_percentage, f"{topic_percentage:.1f}%")
                    status_col1, status_col2 = st.columns(2, gap="small")
                    with status_col1:
                        status_box("PYQ", pyq_status)
                    with status_col2:
                        status_box("Test", test_status)

    # ========================================================
    # NORMAL YEARS
    # ========================================================

    else:

        st.title(year)

        year_progress = get_year_progress(
            year
        )

        progress_bar(
            year_progress,
            f"Year Progress {year_progress:.1f}%"
        )

        st.divider()

        subjects = years[year]

        columns = st.columns(
            3,
            gap="small"
        )

        for i, subject in enumerate(subjects):

            topics = subjects[subject]

            subject_progress = get_subject_overall_progress(
                topics
            )

            with columns[i % 3]:

                with st.container(
                    border=True,
                    key=(
                        "subject_card_"
                        f"{css_key(year)}_"
                        f"{css_key(subject)}"
                    ),
                    gap="small"
                ):

                    if st.button(
                        subject,
                        key=(
                            f"subject_"
                            f"{css_key(year)}_"
                            f"{css_key(subject)}"
                        ),
                        use_container_width=True
                    ):

                        go_subject(
                            year,
                            subject
                        )

                        st.rerun()

                    progress_bar(
                        subject_progress,
                        f"{subject_progress:.1f}%"
                    )

                    subject_pyq_status = topics.get(
                        "subject_pyqs", False
                    )
                    subject_test_status = topics.get(
                        "subject_test", False
                    )

                    status_col1, status_col2 = st.columns(
                        2,
                        gap="small"
                    )
                    with status_col1:
                        status_box(
                            "Subject PYQs",
                            subject_pyq_status
                        )
                    with status_col2:
                        status_box(
                            "Subject Test",
                            subject_test_status
                        )


# ============================================================
# SUBJECT PAGE
# ============================================================

elif st.session_state.selected_page == "subject":

    year = st.session_state.selected_year
    subject = st.session_state.selected_subject

    # ========================================================
    # SUBJECT DETAILS
    # ========================================================

    # ========================================================
    # NORMAL SUBJECT
    # ========================================================


    if year == "Minor":

        topic_data = years[year][subject]
        if not isinstance(topic_data, dict):
            topic_data = {}
            years[year][subject] = topic_data

        if st.button(
            f"← Back to {year}",
            key=f"major_minor_back_{css_key(year)}_{css_key(subject)}"
        ):
            go_year(year)
            st.rerun()

        st.title(subject)
        topic_percentage = get_topic_percentage(topic_data)
        progress_bar(topic_percentage, f"{topic_percentage:.1f}%")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.divider()
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        progress_buttons(topic_data, year, subject, subject, "Notes", "notes")
        st.divider()
        progress_buttons(topic_data, year, subject, subject, "Revision Notes", "revision")
        st.divider()
        progress_buttons(topic_data, year, subject, subject, "Question Banks", "question_banks")
        st.divider()

        col1, col2 = st.columns(2, gap="small")
        with col1:
            pyq = st.checkbox("PYQs", value=topic_data.get("pyqs", False) is True, key=f"mm_pyq_{css_key(year)}_{css_key(subject)}")
        with col2:
            test = st.checkbox("Subject Test", value=topic_data.get("subject_test", False) is True, key=f"mm_test_{css_key(year)}_{css_key(subject)}")

        old_pyq = topic_data.get("pyqs", False) is True
        old_test = topic_data.get("subject_test", False) is True
        if pyq != old_pyq or test != old_test:
            topic_data["pyqs"] = pyq
            topic_data["subject_test"] = test
            save_database(st.session_state.years)

    else:

        topics = years[year][subject]

        if st.button(
            f"← Back to {year}",
            key=(
                f"subject_back_"
                f"{css_key(year)}_"
                f"{css_key(subject)}"
            )
        ):

            go_year(year)

            st.rerun()

        st.title(subject)

        topic_percentage = get_subject_topic_progress_academic(
            topics
        )

        progress_bar(
            topic_percentage,
            f"Topics {topic_percentage:.1f}%"
        )

        st.markdown(
            "<div style='height: 8px;'></div>",
            unsafe_allow_html=True
        )

        pyq_percentage, pyq_fraction = get_pyq_progress(
            topics
        )

        progress_bar(
            pyq_percentage,
            f"Topic Pyqs {pyq_fraction}"
        )

        st.markdown(
            "<div style='height: 8px;'></div>",
            unsafe_allow_html=True
        )

        subject_col1, subject_col2 = st.columns(
            2,
            gap="small"
        )

        with subject_col1:
            subject_pyq = st.checkbox(
                "Subject PYQs",
                value=topics.get("subject_pyqs", False),
                key=(
                    f"subject_pyq_"
                    f"{css_key(year)}_"
                    f"{css_key(subject)}"
                )
            )

        with subject_col2:
            subject_test = st.checkbox(
                "Subject Test",
                value=topics.get("subject_test", False),
                key=(
                    f"subject_test_"
                    f"{css_key(year)}_"
                    f"{css_key(subject)}"
                )
            )

        old_subject_pyq = topics.get("subject_pyqs", False)
        old_subject_test = topics.get("subject_test", False)

        if (
            subject_pyq != old_subject_pyq
            or subject_test != old_subject_test
        ):
            topics["subject_pyqs"] = subject_pyq
            topics["subject_test"] = subject_test
            save_database(st.session_state.years)

        st.divider()

        st.subheader("Topics")

        real_topics = {
            topic_name: topic_data
            for topic_name, topic_data in topics.items()
            if topic_name not in {
                "subject_pyqs",
                "subject_test"
            }
            and isinstance(topic_data, dict)
        }

        if not real_topics:

            st.write(
                "No topics added yet."
            )

        else:

            columns = st.columns(
                3,
                gap="small"
            )

            for i, topic in enumerate(real_topics):

                topic_data = real_topics[topic]

                topic_percentage = get_topic_academic_percentage(
                    topic_data
                )

                pyq_status = topic_data.get(
                    "pyqs",
                    False
                )

                with columns[i % 3]:

                    with st.container(
                        border=True,
                        key=(
                            "topic_card_"
                            f"{css_key(year)}_"
                            f"{css_key(subject)}_"
                            f"{css_key(topic)}"
                        ),
                        gap="small"
                    ):

                        if st.button(
                            topic,
                            key=(
                                f"topic_"
                                f"{css_key(year)}_"
                                f"{css_key(subject)}_"
                                f"{css_key(topic)}"
                            ),
                            use_container_width=True
                        ):

                            go_topic(
                                year,
                                subject,
                                topic
                            )

                            st.rerun()

                        progress_bar(
                            topic_percentage,
                            f"{topic_percentage:.1f}%"
                        )

                        status_box(
                            "Topic Pyq",
                            pyq_status
                        )

# ============================================================
# TOPIC DETAIL PAGE
# ============================================================
elif st.session_state.selected_page == "topic":

    year = st.session_state.selected_year
    subject = st.session_state.selected_subject
    topic = st.session_state.selected_topic

    show_topic_detail(
        year,
        subject,
        topic
    )