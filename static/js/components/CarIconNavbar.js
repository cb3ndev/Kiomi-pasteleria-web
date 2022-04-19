import api from "../api.js";
const carIconNavbar = new Vue({
  delimiters: ["[[", "]]"],
  el: "#car-number-items",
  data() {
    return {
      //dbOrderItems: [],
      numItemscarro: 0,
    };
  },

  created() {
    if (user !== "AnonymousUser") {
      api.getOrderItems().then((orderitems) => {
        //this.dbOrderItems = orderitems;
        this.numItemscarro = orderitems.length;
      });
    } else {
      const cartCookie = this.getCookie("cart");
      this.numItemscarro = cartCookie.length;
    }
    console.log(this.numItemscarro);
    console.log(user);
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
  },
});

export { carIconNavbar };
