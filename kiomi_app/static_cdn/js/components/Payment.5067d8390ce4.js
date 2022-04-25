import api from "../api.js";
new Vue({
  delimiters: ["[[", "]]"],
  el: "#payment",
  data() {
    return {
      paymentId: "",
      status: "",
      statusDetail: "",
      //email: "",
    };
  },
  created() {
    /* api.getOrderItems().then((orderItems) => {
      this.dbOrderItems = orderItems;
    }); */
    /* if (user === "AnonymousUser") {
      const cookies = this.getCookieEmail("email");
      this.email = cookies;
    } */
    //console.log(this.getCookie("cart"));
    this.URLDetails();
    //this.updateStatusPayment();

    /* setTimeout(function () {
      checkoutVueInstance.$destroy();
    }, 50); */
  },
  methods: {
    /* getCookieEmail(cName) {
      //NOTA LEER:
      //Esta funcion es un poco diferente a las que estan (getCoookie) en los demas componentes js
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
        return "";
      }
      return res;
    }, */
    URLDetails() {
      const search = window.location.search;
      if (!window.location.search) {
        return console.log("NO DATA");
      }

      const urlParam = new URLSearchParams(search);
      this.paymentId = urlParam.get("payment_id");
      if (urlParam.get("status") === "null") {
        this.status = "rejected";
      } else {
        this.status = urlParam.get("status");
      }

      this.statusDetail = urlParam.get("status_detail");

      console.log(this.status);
      //api.postProcessPaymentOrder(newPaymentStatus);
      //
    },
    /* updateStatusPayment() {
      const newPaymentStatus = {
        status: "approved",
      };

      const response = api.postProcessPaymentOrder(newPaymentStatus);
      console.log(response);
      console.log("orden_cerrada");
    }, */
  },
});
