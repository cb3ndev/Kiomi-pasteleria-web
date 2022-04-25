//const url = "http://127.0.0.1:8000/api";
const url = "https://kiomi-test-v1.herokuapp.com/api";

const getProducts = (currentPage) => {
  const endpoint = `${url}/products/?page=${currentPage}`;
  return fetch(endpoint)
    .then((res) => res.json())
    .then((res) => res);
};
/* Product Details */
const getProductDetails = (id) => {
  const endpoint = `${url}/products-detail/${id}/`;
  return fetch(endpoint)
    .then((res) => res.json())
    .then((res) => res);
};

const getOrderItems = () => {
  const endpoint = `${url}/order-item-get/`;
  return fetch(endpoint)
    .then((res) => res.json())
    .then((res) => res);
};

/* Este fetch fue creado para hacer uso del metodo GET pero
del api order-item-post, este se requiere para hacer el update en el carrito */
const getOrderItemUpdate = (id) => {
  const endpoint = `${url}/order-item-post/${id}/`;
  return fetch(endpoint)
    .then((res) => res.json())
    .then((res) => res);
};

const postProductOrderItems = (orderItems) => {
  const payload = JSON.stringify(orderItems);
  const endpoint = `${url}/order-item-post/`;
  const csrfToken = Cookies.get("csrftoken");
  console.log(csrfToken);
  const headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrfToken,
  };
  const requestOptions = {
    method: "POST",
    headers,
    body: payload,
  };
  return fetch(endpoint, requestOptions)
    .then((response) => {
      if (response.ok) {
        alert("Se ha añadido el item al carrito!");
        return response.json();
      } else {
        alert("Algo salió mal, intente otra vez");
        throw new Error("Algo salio mal");
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

const putProductOrderItems = (orderItems, id) => {
  const payload = JSON.stringify(orderItems);
  const endpoint = `${url}/order-item-post/` + id + `/`;
  const csrfToken = Cookies.get("csrftoken");
  console.log(csrfToken);
  const headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrfToken,
  };
  const requestOptions = {
    method: "PUT",
    headers,
    body: payload,
  };
  return fetch(endpoint, requestOptions)
    .then((res) => res.json())
    .then((res) => res);
};

const deleteProductOrderItems = (id) => {
  const endpoint = `${url}/order-item-post/` + id + `/`;
  const csrfToken = Cookies.get("csrftoken");
  const headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrfToken,
  };
  const requestOptions = {
    method: "DELETE",
    headers,
    body: null,
  };
  return (
    fetch(endpoint, requestOptions)
      //.then((res) => res.json())
      .then((res) => res.text())
      .then((res) => console.log(res))
  );
};

const getCustomer = () => {
  const endpoint = `${url}/customer/`;
  return fetch(endpoint)
    .then((res) => res.json())
    .then((res) => res);
};
const putCustomer = (customer, id) => {
  const payload = JSON.stringify(customer);
  const endpoint = `${url}/customer/` + id + `/`;
  const csrfToken = Cookies.get("csrftoken");
  console.log(csrfToken);
  const headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrfToken,
  };
  const requestOptions = {
    method: "PUT",
    headers,
    body: payload,
  };
  return fetch(endpoint, requestOptions)
    .then((response) => {
      if (response.ok) {
        alert("Se ha actualizado los datos del perfil");
        return response.json();
      } else {
        alert("Algo salió mal, intente otra vez");
        throw new Error("Algo salio mal");
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

export default {
  getProducts,
  getProductDetails,
  postProductOrderItems,
  getOrderItems,
  putProductOrderItems,

  deleteProductOrderItems,

  getOrderItemUpdate,
  getCustomer,

  putCustomer,
};
