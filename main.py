import streamlit as st
import pandas as pd
from PIL import Image
import refresh
#from _db import *
import random
import sqlite3


conn = sqlite3.connect("spare_data.db",check_same_thread=False)
c = conn.cursor()

def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Customer Table create Successfully')

def customer_add_data(Cname,Cpass, Cemail, Cstate,Cnumber):
    c.execute('''INSERT INTO Customers (C_Name,C_Password,C_Email, C_State, C_Number) VALUES(?,?,?,?,?)''', (Cname,Cpass,  Cemail, Cstate,Cnumber))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data
def customer_update(Cemail,Cnumber):
    c.execute(''' UPDATE Customers SET C_Number = ? WHERE C_Email = ?''', (Cnumber,Cemail,))
    conn.commit()
    print("Updating")
def customer_delete(Cemail):
    c.execute(''' DELETE FROM Customers WHERE C_Email = ?''', (Cemail,))
    conn.commit()


def part_delete(pid):
    c.execute(''' DELETE FROM inventory WHERE i_pid = ?''', (pid,))
    c.execute(''' DELETE FROM Parts WHERE P_id = ?''', (pid,))
    conn.commit()


              
def part_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Parts(
                P_Name VARCHAR(50) NOT NULL,
                P_id INT PRIMARY KEY NOT NULL)
                ''')
    print('Part Table create Successfully')

def part_add_data(Pname, Pid,Pqty):
    c.execute('''INSERT INTO Parts (P_Name, P_id) VALUES(?,?)''', (Pname,Pid))
    c.execute('''INSERT INTO inventory (i_pid, i_pname, i_Qty) VALUES(?,?,?)''', (Pid,Pname,Pqty))
    conn.commit()

def part_view_all_data():
    c.execute('SELECT * FROM Parts')
    part_data = c.fetchall()
    return part_data

def inventory_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory(
                i_pid VARCHAR(15) NOT NULL,
                i_pname VARCHAR(20) DEFAULT NULL,
                i_Qty int unsigned DEFAULT NULL,
                primary key(i_pid ),foreign key(i_pid) references Parts(P_id))
    ''')
def inventory_update(pid,pqty):
    c.execute(''' UPDATE inventory SET i_Qty = ? WHERE i_pid = ?''', (pqty,pid))
    conn.commit()

def  countreduce(pid,qty):
    c.execute('''update inventory set i_Qty = ? where i_pid = ?''',(qty,pid))
    conn.commit()

def invt_view_all_data():
    c.execute('SELECT * FROM invento(ry')
    invt_data = c.fetchall()
    return invt_data

def provider():
    c.execute('''CREATE TABLE IF NOT EXISTS Providers(
        prt_id varchar(10) primary key,
        prt_name varchar(20) not null,
        prt_provider_name varchar(50),
        prt_contact number(10) not null check(length(prt_contact)=10,
        foreign key(prt_id) references Parts(P_id)))''')

def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL)
    ''')

def order_delete(Oid):
    c.execute(''' DELETE FROM Orders WHERE O_id = ?''', (Oid,))
    conn.commit()

def order_add_data(O_Name,O_Items,O_Qty,O_id):
    c.execute('''INSERT INTO Orders (O_Name, O_Items,O_Qty, O_id) VALUES(?,?,?,?)''',
              (O_Name,O_Items,O_Qty,O_id))
    conn.commit()


def order_view_data(customername):
    c.execute('SELECT * FROM ORDERS Where O_Name == ?',(customername,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT * FROM ORDERS')
    order_all_data = c.fetchall()
    return order_all_data

def provider_view_all_data():
    c.execute('SELECT * FROM Providers')
    provider_data = c.fetchall()
    return provider_data

def admin():


    st.title("Spare Parts Database Dashboard")
    menu = ["Parts", "Customers", "Orders","Inventory","Providers"]
    choice = st.sidebar.selectbox("Menu", menu)

    ## Parts
    if choice == "Parts":

        menu = ["Add", "View", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":
            st.subheader("Add Parts")
            part_name = st.text_area("Enter the Part Name")
            part_quantity = st.text_area("Enter the quantity")
            part_id = st.text_area("Enter the Part id (example:#D1)")
            if st.button("Add Part"):
                part_add_data(part_name,part_id,part_quantity)
                st.success("Successfully Added Data")

        if choice == "View":
            st.subheader("Part Details")
            part_result = part_view_all_data()
            invt_result = invt_view_all_data()
            with st.expander("View All Part Data"):
                part_clean_df = pd.DataFrame(part_result, columns=["Name","ID"])
                st.dataframe(part_clean_df)
            with st.expander("View Part Quantity"):
                invt_clean_df = pd.DataFrame(invt_result, columns=["Name","ID","Quantity"])
                st.dataframe(invt_clean_df)

        if choice == 'Delete':
            st.subheader("Delete Part")
            did = st.text_area("Part ID")
            if st.button(label="Delete"):
                part_delete(did)
                st.success("Successfully deleted")



    ## CUSTOMERS
    elif choice == "Customers":

        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password","Email-ID" ,"Area", "Number"])
                st.dataframe(cust_clean_df)

        if choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_area("Email")
            cust_number = st.text_area("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email,cust_number)

        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_area("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email)

    elif choice == "Orders":

        menu = ["View","Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID"])
                st.dataframe(order_clean_df)

        elif choice == "Delete":
             st.subheader("Delete Orders")
             oid= st.text_area("OrderId")
             if st.button(label="Delete"):
                order_delete(oid)
            
    elif choice == "Inventory":
            
            menu = ["View","Update"]
            choice = st.sidebar.selectbox("Menu", menu)
            if choice == "View":
                st.subheader("Inventory Details")
                invt_result = invt_view_all_data()
                #st.write(cust_result)
                with st.expander("View All Inventory Data"):
                    invt_clean_df = pd.DataFrame(invt_result, columns=["Name", "ID","Quantity"])
                    st.dataframe(invt_clean_df)
    
            elif choice == "Update":
                st.subheader("Update Inventory")
                pid= st.text_area("Part ID")
                qty= st.text_area("Quantity")
                if st.button(label="Update"):
                    inventory_update(pid,qty)
                    st.success("Successfully updated")
    
    elif choice == "Providers":
        menu = ["View"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "View":
            st.subheader("Provider Details")
            prt_result = provider_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Provider Data"):
                prt_clean_df = pd.DataFrame(prt_result, columns=["Part_ID","Name","Company Name","Contact Number"])
                st.dataframe(prt_clean_df)

       
def getauthenicate(username, password):
    #print("Auth")
    c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?', (username,))
    cust_password = c.fetchall()
    #print(cust_password[0][0], "Outside password")
    #print(password, "Parameter password")
    if cust_password[0][0] == password:
        #print("Inside password")
        return True
    else:
        return False


###################################################################


def customer(username, password):
    if getauthenicate(username, password):
        print("In Customer")
        # st.title("Welcome to Pharmacy Store")

        st.subheader("Your Order Details")
        order_result = order_view_data(username)
        # st.write(cust_result)
        with st.expander("View All Order Data"):
            order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
            st.dataframe(order_clean_df)

        part_result = part_view_all_data()
        invt_result = invt_view_all_data()
        print(part_result)


        st.subheader("Part: "+part_result[0][0])

        img = Image.open('images\Tyre.jpg')
        st.image(img, width=200, caption="per 8000/-")

        if(invt_result[0][2]>0):
            part1 = st.slider(label="Quantity",min_value=0, max_value=5, key= 1)
        else:
            st.info("Out of stock")
        


        st.subheader("Part: " + part_result[1][0])
        img = Image.open('images\mirror.jpg')
        st.image(img, width=200 , caption="per 3500/-")
        if(invt_result[1][2]>0):
            part2 = st.slider(label="Quantity",min_value=0, max_value=5, key= 2)
        else:
            st.info("Out of stock")

       

        st.subheader("Part: " + part_result[2][0])
        img = Image.open('images\headlight.jpg')
        st.image(img, width=200, caption="per 12000 /-")
        if(invt_result[2][2]>0):
            part3=st.slider(label="Quantity",min_value=0, max_value=5, key=3)
        else:
            st.info("Out of stock")
         


        if st.button(label="Buy now"):
            O_items = ""

            if int(part1) > 0:
                O_items += "Dolo-650,"
                countreduce(invt_result[0][2],int(invt_result[0][2])-int(part1))

            if int(part2) > 0:
                O_items += "Strepsils,"
                countreduce(invt_result[1][2],int(invt_result[1][2])-int(part2))
            if int(part3) > 0:
                O_items += "Vicks"
                countreduce(invt_result[2][2],int(invt_result[2][2])-int(part3))
            O_Qty = str(part1) + "," + str(part2) + "," + str(part3)

            

            O_id = username + "#O" + str(random.randint(0,1000000))
            #order_add_data(O_Name, O_Items,O_Qty, O_id):
            order_add_data(username, O_items, O_Qty, O_id)
            st.success("Successfully ordered!")
            st.text('Total amount ='+ str((int(part1)*8000)+(int(part2)*3500)+(int(part3)*12000))+'/-')






if __name__ == '__main__':
    part_create_table()
    cust_create_table()
    order_create_table()
    inventory_create_table()

    hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    menu = ["Login", "SignUp","Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        st.title("Welcome to Spare Parts Store")
        
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            customer(username, password)

    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2, col3 = st.columns(3)

        with col1:
            cust_email = st.text_area("Email ID")
        with col2:
            cust_area = st.text_area("State")
        with col3:
            cust_number = st.text_area("Phone Number")

        if st.button("Signup"):
            if (cust_password == cust_password1):
                customer_add_data(cust_name,cust_password,cust_email, cust_area, cust_number,)
                st.success("Account Created!")
                st.info("Go to Login Menu to login")
            else:
                st.warning('Password dont match')
    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        # if st.sidebar.button("Login"):
        if username == 'admin' and password == 'admin':
            admin()