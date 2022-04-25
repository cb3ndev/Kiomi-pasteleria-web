import api from "../api.js";
new Vue({
  delimiters: ["[[", "]]"],
  el: "#profile",
  data() {
    return {
      dbCustomer: {},
      errors: [],
      isInvalid: {
        name: false,
        lastName: false,
        //email: false,
      },
    };
  },
  created() {
    api.getCustomer().then((dbCustomer) => {
      this.dbCustomer = dbCustomer;
    });
  },
  methods: {
    updateCustomer() {
      api.putCustomer(this.dbCustomer, this.dbCustomer.id);
      console.log("aaa3");
    },

    checkForm(e) {
      e.preventDefault();

      this.errors = [];

      if (
        !this.dbCustomer.name ||
        !this.dbCustomer.lastName /* ||
        !this.dbCustomer.email */
      ) {
        this.isInvalid.name = false;
        this.isInvalid.lastName = false;
        /* this.isInvalid.email = false; */
      } else {
        api.putCustomer(this.dbCustomer, this.dbCustomer.id);
      }
    },
  },
});
