
import streamlit as st

from streamlit_option_menu import option_menu

from tabs import (upload_graph, create_node, update_node, delete_node,
                  create_relation, delete_relation,
                  store_graph, visualization_graph, basic_analyze_graph,
                  export_graph, graph_dict_to_ppr_dict, adv_analyze_graph)

if __name__ == '__main__':
    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []

    if "p1_list" not in st.session_state:
        st.session_state["p1_list"] = []

    if "p2_list" not in st.session_state:
        st.session_state["p2_list"] = []

    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []

    st.session_state["selected_value"] = ""

    st.session_state["selected_value11"] = ""

    st.session_state["selected_value22"] = ""

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

    st.set_page_config(layout="wide")
    with st.sidebar:
        selected_tab = option_menu("Main Menu",
                                   tab_list,
                                   icons=['cloud-download', 'gear', 'brilliance', 'trash', 'asterisk',
                                          'trash-fill',
                                          'clock-history', 'car-front','cast','floppy2', 'cloud-upload'],
                                   menu_icon="cast",
                                   default_index=0,
                                   orientation="vertical"
                                   )

    st.title("PPR - Machine Tower")

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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
