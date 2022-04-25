import api from "../api.js";
import { carIconNavbar } from "./CarIconNavbar.js";
new Vue({
  delimiters: ["[[", "]]"],
  el: "#car",
  data() {
    return {
      dbOrderItems: [],
      subTotal: 0,
      totalQuantityCarItems: 0,
    };
  },
  created() {
    /////////////////////////////////////////
    if (user !== "AnonymousUser") {
      api.getOrderItems().then((orderItems) => {
        this.dbOrderItems = orderItems;
      });
      /////////////////////////////////////77
      ///codigo para obtener la cantidad de productos (suma de los quantitys) al cargar la pagina
      api.getOrderItems().then((orderItems) => {
        if (orderItems.length !== 0) {
          this.totalQuantityCarItems = Object.values(orderItems)
            .map((i) => i.quantity)
            .reduce((a, b) => a + b);
        }
        //console.log(this.totalQuantityCarItems);
      });
    } else {
      const cartCookie = this.getCookie("cart");
      this.dbOrderItems = cartCookie;
      this.dbOrderItems.forEach(function (el, index) {
        api.getProductDetails(el.product).then((product) => {
          //console.log(product.image_1);

          el.id = index;
          el.product = {};
          el.product.image_1 = product.image_1;
          el.product.name = product.name;
          el.product.price = product.price;
          el.product.id = product.id;

          /* el.orderFlavor = product.flavor.flavor;
          el.orderFlavorCoverage = product.flavorCoverage.flavor;
          el.orderFlavorBizcocho = product.flavorBizcocho.flavor; */

          if (el.box_product.length !== 0) {
            el.box_product.forEach(function (galleta) {
              let obj = product.flavor.find(
                (o) => o.id === galleta.orderFlavor
              );
              galleta.orderFlavor = obj.flavor;
            });
          } else {
            if (el.orderFlavor) {
              let obj = product.flavor.find((o) => o.id === el.orderFlavor);
              el.orderFlavor = obj.flavor;
            }
            if (el.orderFlavorCoverage) {
              let obj = product.flavorCoverage.find(
                (o) => o.id === el.orderFlavorCoverage
              );
              el.orderFlavorCoverage = obj.flavor;
            }
            if (el.orderFlavorBizcocho) {
              let obj = product.flavorBizcocho.find(
                (o) => o.id === el.orderFlavorBizcocho
              );
              el.orderFlavorBizcocho = obj.flavor;
            }
          }
        });
      });

      /////////codigo para obtener la cantidad de productos (suma de los quantitys) al cargar la pagina///////
      if (cartCookie.length !== 0) {
        this.totalQuantityCarItems = cartCookie
          .map((i) => i.quantity)
          .reduce((a, b) => a + b);
      }
    }
    console.log("eweeeeeees");
  },
  methods: {
    getCookie(cName) {
      const name = cName + "=";
      const cDecoded = decodeURIComponent(document.cookie);
      const cArr = cDecoded.split("; ");
      let res;
      cArr.forEach((val) => {
        if (val.indexOf(name) === 0) {
          res = val.substring(name.length);
        }
      });
      if (res === undefined) {
        return [];
      }
      return JSON.parse(res);
    },

    //////////////////////
    calcularSubTotal() {
      let auxSubTotal = 0.0;
      this.dbOrderItems.forEach(function (el, index) {
        auxSubTotal += el.product.price * el.quantity;
      });

      this.subTotal = auxSubTotal.toFixed(2);
      return this.subTotal;
    },
    deleteItem(id, indexArray) {
      /* const endpoint = `http://127.0.0.1:8000/api/order-item-post/` + id + `/`;
      const csrfToken = Cookies.get("csrftoken");
      const response = await fetch(endpoint, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: null,
      });

      const data = await response.json();

      // now do whatever you want with the data
      return console.log(data); */

      //console.log(id);
      //const response = api.deleteProductOrderItems(id);
      console.log();
      //console.log(response);
      let quantityEliminado = this.dbOrderItems[indexArray].quantity;
      const newDbOrderItems = this.dbOrderItems.filter((el) => el.id !== id);
      this.dbOrderItems = newDbOrderItems;
      if (user !== "AnonymousUser") {
        api.deleteProductOrderItems(id);
      } else {
        const cartCookie = this.getCookie("cart");
        //const newCartCookie = cartCookie.filter((el, index) => index !== id);
        const newCartCookie = cartCookie.filter(function (value, index) {
          return index !== indexArray;
        });
        document.cookie =
          "cart=" + JSON.stringify(newCartCookie) + ";domain=;path=/";
      }
      carIconNavbar.numItemscarro -= 1;
      this.totalQuantityCarItems -= quantityEliminado; //se le resta la cantidad de elementos del elemento que se elimino
    },

    updateItemQuantity(newQuantity, indexArray, idAtrr) {
      let quantityEliminado = this.dbOrderItems[indexArray].quantity;

      if (
        this.totalQuantityCarItems <= 5 ||
        newQuantity - quantityEliminado < 0
      ) {
        if (user !== "AnonymousUser") {
          const newdbOrderItemUpdate = {
            quantity: newQuantity,
          };

          api.putProductOrderItems(newdbOrderItemUpdate, idAtrr);
        } else {
          const cartCookie = this.getCookie("cart");
          const newCartCookie = cartCookie;
          newCartCookie[indexArray].quantity = newQuantity;

          console.log(newCartCookie);
          document.cookie =
            "cart=" + JSON.stringify(newCartCookie) + ";domain=;path=/";
        }
        this.dbOrderItems[indexArray].quantity = newQuantity;

        if (newQuantity - quantityEliminado > 0) {
          this.totalQuantityCarItems += 1;
        } else {
          this.totalQuantityCarItems -= 1;
        }
      } else {
        setTimeout(function () {
          alert(
            "No se puede añadir mas items al carro, el límite es de 6 productos por compra"
          );
        }, 50);
      }
    },

    canQuantityGoUp(quantity) {
      if (quantity < 6) {
        return true;
      }
      return false;
    },
    canQuantityGoDown(quantity) {
      if (quantity > 1) {
        return true;
      }
      return false;
    },
  },
});
