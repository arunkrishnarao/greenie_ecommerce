# Greenie - a Django Multi-Vendor Website with Razorpay integration

Greenie is a Python-based Django application that serves as a comprehensive e-commerce platform tailored for grocery shopping. With an simple and user-friendly interface, Greenie enables customers to shop for a variety of grocery products from multiple vendors, make secure payments via Razorpay, and receive timely order confirmations. Vendors can effortlessly register, showcase their products, manage orders, and keep track of notifications, creating a seamless experience. The admin dashboard empowers administrators to oversee categories, products, users, and orders, while also facilitating order processing and data export to Excel.

- Screenshot:
![alt text](https://github.com/arunkrishnarao/greenie_ecommerce/blob/main/greenie.png?raw=true)

## Features

- Admin: Admin users have extensive control over categories, products, users, and orders, along with the ability to generate Excel reports and customize frontpage images.

- Vendor Empowerment: Vendors can easily add products, manage their profiles, and receive notifications for incoming orders.

- User Convenience: Customers can browse, add products to cart, make card payments, provide delivery addresses, and receive order confirmation emails.

- Secure Payments: Integration with Razorpay ensures safe and convenient payment processing.


### Pre-Requisites:
1. Install Git Version Control
[ https://git-scm.com/ ]

2. Install Python Latest Version
[ https://www.python.org/downloads/ ]

3. Install Pip (Package Manager)
[ https://pip.pypa.io/en/stable/installing/ ]


### Installation
**1. Create a Project Folder**

**2. Create a python virtual environment and activate it**

* Install Virtual Environment package in python
```
pip install virtualenv
```

* Create Virtual Environment

```
python -m venv venv
```

* Activate Virtual Environment

```
source venv/scripts/activate
```


**3. Clone this project**
```
git clone https://github.com/arunkrishnarao/greenie_ecom.git

cd greenie_ecom
```

**4. Install Requirements**
```
pip install -r requirements.txt
```

**6. Run the Server**
```
python manage.py runserver 8081
```

**7. Login Credentials**

* Create Superuser
```
python manage.py createsuperuser
```

