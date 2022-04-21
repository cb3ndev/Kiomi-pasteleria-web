// import StoreCardProduct from './StoreCardProduct'
//  const currentPage= 1;

import api from "../api.js";
new Vue({
  delimiters: ["[[", "]]"],
  el: "#checkout",
  data() {
    return {
      isLoading: false,
      isActive: false,
      message: "hello",
      dbCheckout: {
        cartItems: 0,
        cartTotal: 0,
        items: [], //Este se usara para pintar
        dbItems: [], //Este se usara para enviar data al backend (en este items los sabores estaran con sus ids y no populados como en "items")
        orderUniqueIdentifier: "",
      },
      nombrePersonaEnvio: "",
      address: "",
      distrito: "",
      phoneNumber: "",
      reference: "",
      email: null, //el correo solo servira para enviar correo si no se esta loggeado
      isInvalid: {
        address: false,
        distrito: false,
        phoneNumber: false,
        nombrePersonaEnvio: false,
        dateDelivery: false,
        email: false, //el correo solo servira para enviar correo si no se esta loggeado
      },
      metodoPago: "yape",
      nombrePagador: "",
      apellidoPagador: "",

      es: vdp_translation_es.js,
      disabledDates: {
        to: null,
        from: null,
        dates: [],
      },
      dateDelivery: null,
      //la data que sigue no se guarda, solo se le envia a mercadopago
      documentoDNI: "",
    };
  },
  //component cdn vuejs-datepicker
  components: {
    vuejsDatepicker,
  },

  created() {
    if (user !== "AnonymousUser") {
      this.getOrderItems();
    } else {
      this.email = ""; //en caso no se este loggeado, el correo se volvera vacio por defecto (dejara de ser nulo como se declaro arriba)
      this.dbCheckout.dbItems = this.getCookie("cart"); //este se usara para enviar a la bd (ver en las variables de vue)
      this.dbCheckout.items = this.getCookie("cart");
      this.dbCheckout.items.forEach(function (el, index) {
        api.getProductDetails(el.product).then((product) => {
          //console.log(product.image_1);

          el.id = index;
          el.product = {};
          el.product.image_1 = product.image_1;
          el.product.name = product.name;
          el.product.price = product.price;
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

      this.dbCheckout.cartItems = this.dbCheckout.items.length;
      //this.dbCheckout.orderUniqueIdentifier = "awa123"; //cuando no se esta loggeado se le dara el valor despues
      //en el post validateShipping
    }
  },

  methods: {
    calcularTotal() {
      if (user == "AnonymousUser") {
        if (this.dbCheckout.items.length !== 0) {
          this.dbCheckout.cartTotal = this.dbCheckout.items
            .map((i) => i.quantity * i.product.price)
            .reduce((a, b) => a + b);
        }
      }
      return this.dbCheckout.cartTotal.toFixed(2);
    },
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
    async getOrderItems() {
      try {
        this.isLoading = true;
        let final = "/api/checkout/";
        if (window.location.hostname === "127.0.0.1") {
          final = ":8000/api/checkout/";
        }
        const startUrl = window.location.protocol
          .concat("//")
          .concat(window.location.hostname);
        const url = `${startUrl}${final}`;
        console.log("yep url: ", url);
        const res = await fetch(url);
        const data = await res.json();
        // console.log('yep data', data);
        this.dbCheckout = data;
        this.isLoading = false;
      } catch (err) {
        // console.log('yep err: ', err)
        this.isLoading = false;
      }
    },
    async handleContinue(e) {
      e.preventDefault();

      // VALIDANDO LOS INPUTS
      if (user === "AnonymousUser") {
        this.isInvalid.email = !this.validarEmail(this.email);
      }

      this.isInvalid.nombrePersonaEnvio = !(
        this.nombrePersonaEnvio.trim().length > 3
      );
      this.isInvalid.address = !(this.address.trim().length > 3);
      this.isInvalid.distrito = !(this.distrito.trim().length > 3);
      // const regExpFullName    =  /^[a-zA-ZáéíóúÁÉÍÓÚ]{2,15}(?: [a-zA-ZáéíóúÁÉÍÓÚ]+)?(?: [a-zA-ZáéíóúÁÉÍÓÚ]+)?(?: [a-zA-ZáéíóúÁÉÍÓÚ]+)?$/
      // this.isInvalid.nombrePersonaEnvioRegEx = regExpFullName.test( this.nombrePersonaEnvio )
      const regExpPhoneNumber = /[+0123456789]{6,12}/;
      this.isInvalid.phoneNumber = !regExpPhoneNumber.test(this.phoneNumber);

      if (this.dateDelivery) {
        this.isInvalid.dateDelivery = false;
      } else {
        this.isInvalid.dateDelivery = true;
      }

      if (
        !this.isInvalid.nombrePersonaEnvio &&
        !this.isInvalid.address &&
        !this.isInvalid.distrito &&
        !this.isInvalid.phoneNumber &&
        !this.isInvalid.dateDelivery &&
        !this.isInvalid.email
      ) {
        const shippingInfo = {
          nombrePersonaEnvio: this.nombrePersonaEnvio,
          address: this.address,
          distrito: this.distrito,
          phoneNumber: this.phoneNumber,
          reference: this.reference,
          identificador: this.dbCheckout.orderUniqueIdentifier,
        };
        console.log(JSON.stringify(shippingInfo));
        try {
          this.isLoading = true;
          let final = "/api/validate-shipping/";
          if (window.location.hostname === "127.0.0.1") {
            final = ":8000/api/validate-shipping/";
          }
          const startUrl = window.location.protocol
            .concat("//")
            .concat(window.location.hostname);
          const url = `${startUrl}${final}`;
          // console.log('yep url: ', url)
          const csrfToken = Cookies.get("csrftoken");
          const options = {
            method: "POST",
            headers: {
              "Content-type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(shippingInfo),
          };
          const res = await fetch(url, options);
          const data = await res.json();
          // console.log('res', res);

          if (user !== "AnonymousUser")
            console.log("post shiping address correcto", data.shipping_saved);
          else {
            console.log(
              "post shiping address correcto, identificador:",
              data.orderUniqueIdentifier
            );
            this.dbCheckout.orderUniqueIdentifier = data.orderUniqueIdentifier;

            document.cookie = "email=" + this.email + ";domain=;path=/";
          }
          this.isLoading = false;
        } catch (err) {
          console.log("yep err: ", err);
          this.isLoading = false;
        }

        this.isActive = true;
      } else {
        this.isActive = false;
      }
    },
    async handlePayment(e) {
      e.preventDefault();
      const ProcessOrderInfo = {
        total: this.dbCheckout.cartTotal,
        metodoPago: this.metodoPago,
        nombrePagador: this.nombrePagador,
        apellidoPagador: this.apellidoPagador,
        documentoDNI: this.documentoDNI,
        dateDelivery: this.dateDelivery.getTime(),
      };
      if (user === "AnonymousUser") {
        ProcessOrderInfo.items = this.dbCheckout.dbItems;
        ProcessOrderInfo.identificador = this.dbCheckout.orderUniqueIdentifier;
      }

      try {
        this.isLoading = true;
        let final = "/api/process-order/";
        if (window.location.hostname === "127.0.0.1") {
          final = ":8000/api/process-order/";
        }
        const startUrl = window.location.protocol
          .concat("//")
          .concat(window.location.hostname);
        const url = `${startUrl}${final}`;
        // console.log('yep url: ', url)
        const csrfToken = Cookies.get("csrftoken");
        const options = {
          method: "POST",
          headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify(ProcessOrderInfo),
        };
        const res = await fetch(url, options);
        const data = await res.json();
        console.log("yep data", data);
        ///////////////
        /* const mp = new MercadoPago(
          "TEST-1dbd5cfc-65a3-43ba-b6e0-589b0dac468e",
          {
            locale: "es-PE",
          }
        );
        const checkout = mp.checkout({
          preference: {
            id: data["id"],
          },
          autoOpen: true, // Habilita la apertura automática del Checkout Pro
        }); */

        if (this.metodoPago === "tarjeta") {
          window.location.href = data["init_point"];
        } else if (this.metodoPago === "yape") {
          window.location.href =
            "/payment/?status=pending&dateDelivery=" +
            this.dateDelivery.getTime() +
            "&identificador=" +
            this.dbCheckout.orderUniqueIdentifier;
        } else {
          window.location.href =
            "/payment/?status=pending&dateDelivery=" +
            this.dateDelivery.getTime() +
            "&identificador=" +
            this.dbCheckout.orderUniqueIdentifier;
        }
        //NOTA (ver arriba): En caso de la tarjeta la fecha se enviara por el url cuando el pago sea exitoso
        //en caso de yape se enviara directamente aqui, esto lo recivira el views de "payment" y lo posteara en order
        //alert("Transaccion completada"); NOTAR que se envia la fecha en formato integer (getTime())
        this.isLoading = false;
      } catch (err) {
        console.log("yep err: ", err);
      }
    },

    changePaymentMethod(method) {
      this.metodoPago = method;
      // console.log(this.imgPrincipal);
    },
    async getDates() {
      try {
        this.isLoading = true;
        let final = "/api/Date-Picker/";
        if (window.location.hostname === "127.0.0.1") {
          final = ":8000/api/Date-Picker/";
        }
        const startUrl = window.location.protocol
          .concat("//")
          .concat(window.location.hostname);
        const url = `${startUrl}${final}`;
        console.log("yep url: ", url);
        const res = await fetch(url);
        const data = await res.json();
        console.log("yep data", data);
        // this.dbCheckout = data;

        //add invalid dates dates
        let prototipeInvalidDates = data.invalid_dates;
        this.disabledDates.dates = prototipeInvalidDates.map(
          (date) => new Date(date)
        );
        //add fecha de desabilitada desde
        this.disabledDates.to = new Date(data.to_date);
        //add fecha desabilitada hasta
        this.disabledDates.from = new Date(data.from_date);
        //add domingos desabilitados
        let prototipeDisabledSundays = data.disabled_sundays;
        this.disabledDates.dates = [
          ...this.disabledDates.dates,
          ...prototipeDisabledSundays.map((date) => new Date(date)),
        ];
        this.isLoading = false;
      } catch (err) {
        // console.log('yep err: ', err)
        this.isLoading = false;
      }
    },
    handleContinueDate() {
      this.getDates();
    },

    validarEmail(value) {
      var input = document.createElement("input");

      input.type = "email";
      input.required = true;
      input.value = value;

      return typeof input.checkValidity === "function"
        ? input.checkValidity()
        : /\S+@\S+\.\S+/.test(value);
    },
  },
});
