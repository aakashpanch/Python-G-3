
import streamlit as st

from streamlit_option_menu import option_menu


from tabs import (upload_graph, create_node, update_node, delete_node, create_relation, delete_relation, store_graph, visualization_graph, analyze_graph,

                  export_graph)

if __name__ == '__main__':
    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []
    # if "node_list1" not in st.session_state:  # node_list1 - data from imported JSON file
    # st.session_state["node_list1"] = []
    if "p1_list" not in st.session_state:
        st.session_state["p1_list"] = []
    # if "edge_list1" not in st.session_state:  # edge_list1 - data from imported JSON file
    #  st.session_state["edge_list1"] = []
    if "p2_list" not in st.session_state:
        st.session_state["p2_list"] = []
    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []
    st.session_state["selected_value"] = ""
    st.session_state["selected_value11"] = ""

    tab_list = [
            "Import existing graph",
            "Create Nodes",
            "Update Nodes",
            "Delete Nodes",
            "Create Relation",
            "Delete Relation",
            "Store the graph",
            "Visualize the graph",
            "Analyze the graph",
            "Export the graph"
        ]

    st.set_page_config(layout="wide")
    with st.sidebar:
        selected_tab = option_menu("Main Menu",
                                   tab_list,
                                   icons=['upload', 'node-plus-fill', 'arrow-repeat', 'trash', 'diagram-3-fill', 'trash3-fill',
                                          'floppy2', 'graph-up', 'bezier2', 'download'],
                                   menu_icon="",
                                   default_index=0,
                                   orientation="vertical"
                                   )

    #selected_tab = option_menu("Main Menu",
                          #     tab_list,
                        #       icons=['house', 'gear', 'arrow-clockwise','apple','asterisk','balloon','boombox'],
                         #      menu_icon="cast",
                          #     default_index=1,
                          #     orientation= "horizontal"
                           #    )
    
    st.title("PPR-Machine Tower")

    if selected_tab == "Import existing graph":
       upload_graph()

    if selected_tab == "Create Nodes":
        create_node()
    
    if selected_tab == "Update Nodes":
        update_node()

    if selected_tab == "Delete Nodes":
        delete_node()

    if selected_tab ==  "Create Relation":
        create_relation()

    if selected_tab == "Delete Relation":
        delete_relation()
  
    if selected_tab == "Store the graph":
        store_graph()

    if selected_tab ==  "Visualize the graph":
        visualization_graph()

    if selected_tab ==  "Analyze the graph":
        analyze_graph()

    if selected_tab ==  "Export the graph":
        export_graph()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
