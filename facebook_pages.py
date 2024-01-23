import facebook as fb
import requests
import streamlit as st
import io
import os
from dotenv import load_dotenv
from os import getenv

from selenium_bot import post_to_facebook
from main_page_functions import delete_items
from Facebook_chain import Facebook_Bot
from comment_in_groups import comment_in_posts

load_dotenv()
access_token = "EAAkXqVLdvigBOyZC6FNtXoI6bXoNGGfcLkqPVvOUCIQf7NaCkQNEQM8uf76TeUPAds3LmXrbqmdyDHRhJPM7XMm0WQHPIBCyFVsZB4I5XlfL74ByF4RfkYa8koJznHgDwRLG7JZACCFsVuZARv2DG2sD98ZA9IDrmP2PzdgPUd5lRAhyzzmGTZCQGomeMXHCq0ZC0iLI3poSs1GK39LnU9nB6VQwgsYUsQG4vJ6UM4PFG5QDXsHf7HZBJuoaF6yjYl1HaxOvOgZDZD"

st.session_state.testfb = fb.GraphAPI(access_token=access_token)

st.set_page_config(layout="wide")

if "post_list" not in st.session_state:
    st.session_state.post_list = []

if "salvot" not in st.session_state:
    st.session_state.salvot = Facebook_Bot()
    print("salvot created")
    
if "comment_list" not in st.session_state:
    st.session_state.comment_list = []

# Crea una columna para colocar el encabezado arriba
st.header("Post to Facebook 🔼")

tab_own_post, tab_group_post, comment_posts = st.tabs(["Post on your own page", "Post on Facebook Groups", "Comment on Facebook posts"])

# Crea dos columnas para los elementos de entrada

with st.sidebar:
    session_container = st.container()
    st.session_state.username = session_container.text_input("Enter your Facebook email:", key="email")
    password = session_container.text_input("Enter your Facebook password:", key="password", type="password")
    login = session_container.button("Login to Facebook")
    if login:
        if not st.session_state.username and not password:
            st.warning("Please enter your Facebook email and password")
        elif password and not st.session_state.username:
            st.warning("Please enter your Facebook email")
        elif st.session_state.username and not password:
            st.warning("Please enter your Facebook password")
        else:
            st.success("Logged in successfully!")
            
with tab_own_post:
    own_container = st.container()
    col1, col2 = own_container.columns([2, 1])

    # Elementos en la primera columna
    with col1:
        col1_container = st.container()
        ai_texts = col1_container.text_input(label="Tell your ideas to SALVot",placeholder="Tell SALVot what topic do you want to talk about in your Facebook post")
        test = col1_container.text_area("Write something to post to Facebook", height=200)

    # Elementos en la segunda columna
    with col2:
        col2_container = st.container()
        images = col2_container.file_uploader("Upload a picture to post to Facebook", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
        add_to_list = col2_container.button("Add post to list")
        upload = col2_container.button("Upload Posts🔼")

        if add_to_list:
            if ai_texts:
                st.session_state.salvot.get_examples(query= ai_texts)
                response = st.session_state.salvot.run_chain(ai_texts)
                response = [str(post) for post in response.split(',\n')]
                for post in response:
                    st.session_state.post_list.append({'text':post, 'images':None})
                print(response)
                
            elif test and images:
                st.session_state.post_list.append({'text':test, 'images':images})
            elif test and not images:
                st.session_state.post_list.append({'text':test, 'images': None})
            else:
                col2_container.warning("Please write something to post to Facebook")
                    
        
        if upload:
            folder_path = "./facebook_images"
            folder_name = "facebook_images"
            if os.path.exists(folder_name):
                delete_items(folder_path)
            for post in st.session_state.post_list:
                if post['text'] and not post['images'] == None:
                    image_bytes = io.BytesIO(post['images'].read())
                    post_number = len(st.session_state.post_list)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    image_path = os.path.join(folder_path, f"{post_number}.jpg")
                    with open(image_path, "wb") as f:
                        f.write(image_bytes.getvalue())           
                    st.session_state.testfb.put_photo(image=open(image_path,'rb'), message=post['text'])
                    col2_container.success("Posted to Facebook")
                elif post['text']:
                    st.session_state.testfb.put_object(parent_object='me', connection_name='feed', message=post['text'])
                    col2_container.success("Posted to Facebook")

                else:
                    col2_container.warning("Please write something to post to Facebook")

            
            if os.path.exists(folder_name):
                delete_items(folder_path)
        
    print(st.session_state.post_list)


    if st.session_state.post_list:
        own_container.subheader("Your posts to Facebook 🔼")
        
        # Crear una copia de la lista para realizar ediciones
        edited_posts = st.session_state.post_list.copy()
        
        for i, post in enumerate(edited_posts):
            new_text = own_container.text_area(f"Edit Post {i + 1}", value=post['text'], key=f"edit_{i}", height=200)
            
            if new_text:
                post['text'] = new_text

            new_image = own_container.file_uploader(f"Upload a new image for Post {i + 1}", type=["png", "jpg", "jpeg"], accept_multiple_files=False, key=f"image_{i}")
            if new_image:
                post['images'] = new_image

        save_button = own_container.button("Save Posts")

        if save_button:
            # Actualizar la lista original con los cambios
            st.session_state.post_list = edited_posts
            own_container.success("Changes saved successfully!")

    else:
        own_container.warning("You haven't added any posts to Facebook yet")

with tab_group_post:
        
    group_container = st.container()
    group_col1, group_col2 = group_container.columns([2, 1])
 
    with group_col1:
        group_col1_container = st.container()
        group_ai_texts = group_col1_container.text_input(label="Tell your ideas to SALVot!",placeholder="Tell SALVot what topic do you want to talk about in your Facebook post in groups")
        group_test = group_col1_container.text_area("Write something to post to Facebook:", height=200)

        group_add_to_list = group_col1_container.button("Add post to list of posts")
        group_upload = group_col1_container.button("Upload Posts to Facebook🔼")
        
    with group_col2:
        group_col2_container = st.container()
        
        st.session_state.facebook_groups = group_col2_container.text_area("Enter the links of the Facebook groups you want to post to (one per line):", height=200)
        if default_list_button:= group_col2_container.button("Use default list of groups"):
            facebook_default_links = ['https://www.facebook.com/groups/7528611667154183',
                                      'https://www.facebook.com/groups/272181219129669']
            st.session_state.facebook_groups = "\n".join(facebook_default_links)
            default_links = group_col2_container.text_area("Default list of groups:", value=st.session_state.facebook_groups, height=200)
            print("Default links: ", facebook_default_links)
            
        if set_groups:= group_col2_container.button("Set Facebook groups"):
            lines = st.session_state.facebook_groups.split('\n')
            print(st.session_state.facebook_groups)
            st.session_state.facebook_links = [line.strip() for line in lines if line.strip()]
            print("GROUPS SETTED: ", st.session_state.facebook_links)
            
        if group_add_to_list:
            if group_ai_texts:
                st.session_state.salvot.get_examples(query= group_ai_texts)
                groups_response = st.session_state.salvot.run_chain(group_ai_texts)
                groups_response = [str(post) for post in groups_response.split(',\n')]
                for post in groups_response:
                    st.session_state.post_list.append({'text':post, 'images':None})
                print(groups_response)
                
            elif group_test:
                st.session_state.post_list.append({'text':group_test, 'images': None})
            else:
                group_col2_container.warning("Please write something to post to Facebook.")
        
        if group_upload:
            folder_path = "./facebook_images"
            folder_name = "facebook_images"
            if os.path.exists(folder_name):
                delete_items(folder_path)
            for post in st.session_state.post_list:
                if post['text']:
                    html_code = post_to_facebook(post['text'], st.session_state.username, password, st.session_state.facebook_links)
                    print(html_code)
                else:
                    col2_container.warning("Please write something to post to Facebook")
                    
    if st.session_state.post_list:
        group_container.subheader("Your posts to Facebook 🔼")
        
        # Crear una copia de la lista para realizar ediciones
        groups_edited_posts = st.session_state.post_list.copy()
        
        for i, post in enumerate(groups_edited_posts):
            new_text_groups = group_container.text_area(f"Edit Post {i + 1}", value=post['text'], key=f"group_edit_{i}", height=200)
            
            if new_text_groups:
                post['text'] = new_text_groups

        save_button = group_container.button("Save Post")

        if save_button:
            # Actualizar la lista original con los cambios
            st.session_state.post_list = groups_edited_posts
            group_container.success("Changes saved successfully!")

    else:
        group_container.warning("You haven't added any posts to Facebook yet")
        
        
with comment_posts:
    comment_container = st.container()
    comment_col1, comment_col2 = comment_container.columns([2, 1])
    
    
    with comment_col1:
        comment_groups = comment_col1.text_area("Enter the links of the Facebook posts you want to comment on (one per line):", height=200)
   
        if st.session_state.comment_list:
            comment_col1.subheader("Your comments to Facebook posts🔼")
            
            # Crear una copia de la lista para realizar ediciones            
            for i, post in enumerate(st.session_state.comment_list):
                comment_col1.markdown(post["post"])
                comment_col1.markdown(post["comment"])
        else:
            comment_col1.warning("You haven't commented in any Facebook post yet")
        
    with comment_col2:
        set_groups = comment_col2.button("Set Facebook posts")
        
        start_comment = comment_col2.button("Start commenting")
        
        if set_groups:
            lines = comment_groups.split('\n')
            print(comment_groups)
            st.session_state.facebook_links = [line.strip() for line in lines if line.strip()]
            print("GROUPS SETTED: ", st.session_state.facebook_links)

        if start_comment:
            comment_in_posts(st.session_state.facebook_links, st.session_state.username, password)
            


