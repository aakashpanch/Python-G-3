import streamlit as st

# Custom modules
from streamlit_option_menu import option_menu  # Import custom option menu
from tabs import (upload_graph, create_node, update_node, delete_node,  # Import custom tab functions
                  create_relation, delete_relation,
                  store_graph, visualization_graph, basic_analyze_graph,
                  export_graph, graph_dict_to_ppr_dict, adv_analyze_graph)

if __name__ == '__main__':
    # Initialize session state variables if not already present
    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []

    if "p1_list" not in st.session_state:
        st.session_state["p1_list"] = []

    if "p2_list" not in st.session_state:
        st.session_state["p2_list"] = []

    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []

    st.session_state["selected_value"] = ""  # Initialize selected value state variable
    st.session_state["selected_value11"] = ""  # Initialize selected value 11 state variable
    st.session_state["selected_value22"] = ""  # Initialize selected value 22 state variable

    # List of tabs for the sidebar option menu
    tab_list = [
        "Import existing graph",
        "Create Nodes",
        "Update Nodes",
        "Delete Nodes",
        "Create Relation",
        "Delete Relation",
        "Store the graph",
        "Visualize the graph",
        "Basic Analysis of the graph",
        "Advanced Analysis of the graph",
        "Export the graph"
    ]

    # Configure the Streamlit page layout
    st.set_page_config(layout="wide")

    # Sidebar menu to select the main menu tab
    with st.sidebar:
        selected_tab = option_menu("Main Menu",
                                   tab_list,
                                   icons=['cloud-download', 'gear', 'brilliance', 'trash', 'asterisk', 'trash-fill',
                                          'clock-history', 'car-front', 'cast', 'floppy2', 'cloud-upload'],
                                   menu_icon="cast",
                                   default_index=0,
                                   orientation="vertical")

    # Main title for the application
    st.title("PPR - Machine Tower")

    # Determine the action based on the selected tab
    if selected_tab == "Import existing graph":
        upload_graph()

    if selected_tab == "Create Nodes":
        create_node()

    if selected_tab == "Update Nodes":
        update_node()

    if selected_tab == "Delete Nodes":
        delete_node()

    if selected_tab == "Create Relation":
        create_relation()

    if selected_tab == "Delete Relation":
        delete_relation()

    if selected_tab == "Store the graph":
        store_graph()

    if selected_tab == "Visualize the graph":
        visualization_graph()

    if selected_tab == "Basic Analysis of the graph":
        basic_analyze_graph()

    if selected_tab == "Advanced Analysis of the graph":
        adv_analyze_graph()

    if selected_tab == "Export the graph":
        export_graph()
