import api from "../api.js";
import { LocalStorage } from "../utils/LocalStorage.js";
import { carIconNavbar } from "./CarIconNavbar.js";

new Vue({
  delimiters: ["[[", "]]"],
  el: "#product-details",
  data() {
    return {
      arr: [],
      dbProductDetails: [],
      imgPrincipal: 0,
      dbOrderItem: {},
      flavor: "",
      flavorBizcocho: "",
      flavorCobertura: "",
      orderItems: {
        quantity: 1,
        product: null,
        orderFlavorCoverage: null,
        orderFlavorBizcocho: null,
        orderFlavor: null,
        validateOrderItem: true,
        box_product: [],
      },

      /*  orderItemCookies: {
        quantityCookies: 0,
        quantity: 1,
        product: 0,
        orderFlavor: 0,
      }, */

      NumberItemsCookies: [],
      galletasDentroDeCaja: 0,
      selectCookies: [0, 6, 12, 18, 24, 30, 36],
      totalQuantityCarItems: 0, //añadido para que se pueda asignar su valor dentro del "then" de su función
      //valores por defecto solo para galletas, tener en cuenta que estos valores son estaticos, deben ser cambiados cada vez que
      //se aumenten o se disminuyan sabores a las galletas.
      cantidadPorDefectoGalletas: [6, 6, 6, 6, 12], //debe tener la misma cantidad de valores que la cantidad de sabores
      //OJO: NO PONER 0 COMO VALOR POR DEFECTO
    };
  },
  created() {
    /////////////////////////////////////77
    ///codigo para obtener la cantidad de productos (suma de los quantitys) al cargar la pagina
    if (user !== "AnonymousUser") {
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
      if (cartCookie.length !== 0) {
        this.totalQuantityCarItems = cartCookie
          .map((i) => i.quantity)
          .reduce((a, b) => a + b);
      }
    }
    /////////////////////////////////////////
    const newArr = this.getCookie("cart");
    this.arr = newArr;
    /*
			Obtener los detalles del producto de la api
		*/
    api.getProductDetails(this.idDetails()).then((product) => {
      this.dbProductDetails = product;
      //Las tres lineas de abajo guardan en una lista todos los sabores correspondientes al producto elegido
      //Estas tres variables solo sirven para pinta en la plantilla HTML
      this.flavor = product.flavor;
      this.flavorBizcocho = product.flavorBizcocho;
      this.flavorCoverage = product.flavorCoverage;

      //Para el caso de flavor, solo se le asignara un valor siempre y cuando no sea galleta (en la galleta los flavors se añaden en box_product)
      if (this.flavor.length !== 0 && product.categoria.code !== "2") {
        this.orderItems.orderFlavor = product.flavor[0].id;
      }
      if (this.flavorBizcocho.length !== 0) {
        this.orderItems.orderFlavorBizcocho = product.flavorBizcocho[0].id;
      }
      if (this.flavorCoverage.length !== 0) {
        this.orderItems.orderFlavorCoverage = product.flavorCoverage[0].id;
      }
      this.orderItems.product = product.id;

      if (product.categoria.code === "2") {
        //Aqui se le asignara los valores por defecto a lista NumberItemCookies para que funcione bien el código
        //esto es solo para galletas
        this.orderItems.orderFlavor = null;
        product.flavor.forEach((element, index) => {
          this.NumberItemsCookies.push([
            element.id,
            this.cantidadPorDefectoGalletas[index],
          ]);
        });
        this.galletasDentroDeCaja = this.calcularNumeroDeGalletas(
          this.NumberItemsCookies
        );
      }
    });
  },
  watch: {
    /*
     * Observa cambios en quantiy
     */
    quantity(newValue) {
      this.addDbOrderItem("quantity", newValue);
    },
    /*
     * Observa cambios en flavor
     */
    flavor(newValue) {
      this.addDbOrderItem("flavor", newValue);
    },
  },
  methods: {
    /**
     * Get cookies of navigator
     * @param {String} cName
     * @returns if does not exist cookie is empty array
     */
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
    /*
     * @onclick para hacer un post del order item creado
     */
    handleCreateOrderItem() {
      if (this.totalQuantityCarItems + this.orderItems.quantity <= 6) {
        // user is logged ?
        if (user !== "AnonymousUser") {
          this.orderItems.validateOrderItem = true;
          console.log(this.orderItems);
          api.postProductOrderItems(this.orderItems);
          carIconNavbar.numItemscarro += 1;
          this.totalQuantityCarItems += this.orderItems.quantity;
        } else {
          const newArr = this.getCookie("cart");
          this.arr = newArr;

          // console.log("order items " ,this.orderItems);
          // console.log("antes de añadir",this.arr);
          this.arr = [...this.arr, this.orderItems];
          // console.log("añadiendo al arr ", this.arr);
          document.cookie =
            "cart=" + JSON.stringify(this.arr) + ";domain=;path=/";
          console.log("no logged");
          carIconNavbar.numItemscarro += 1;
          this.totalQuantityCarItems += this.orderItems.quantity;
          setTimeout(function () {
            alert("Se ha añadido el item al carrito!");
          }, 80);
        }
      } else {
        setTimeout(function () {
          alert(
            "No se puede añadir mas items al carro, el límite es de 6 productos por compra"
          );
        }, 60);
      }
    },
    /*
     * @onchange para hacer un post orderitemcookies
     */
    handleCreateOrderItemCookies(e, flavorid) {
      if (this.NumberItemsCookies.length === 0) {
        this.NumberItemsCookies.push([flavorid, parseInt(e.target.value)]);
      } else {
        let index = this.NumberItemsCookies.findIndex(
          (el) => el[0] === flavorid
        );
        if (index === -1) {
          this.NumberItemsCookies.push([flavorid, parseInt(e.target.value)]);
        } else {
          if (parseInt(e.target.value) === 0) {
            const newNumberItemsCookies = this.NumberItemsCookies.filter(
              function (valor, indice) {
                return indice !== index;
              }
            );
            this.NumberItemsCookies = newNumberItemsCookies;
          } else {
            this.NumberItemsCookies[index][1] = parseInt(e.target.value);
          }
        }
      }

      this.galletasDentroDeCaja = this.calcularNumeroDeGalletas(
        this.NumberItemsCookies
      );
    },
    validateOrderItemCookies() {
      if (this.totalQuantityCarItems + this.orderItems.quantity <= 6) {
        if (user !== "AnonymousUser") {
          this.orderItems.box_product = this.NumberItemsCookies;
          console.log(this.orderItems);

          api.postProductOrderItems(this.orderItems).then(() => {
            carIconNavbar.numItemscarro += 1;
            this.totalQuantityCarItems += this.orderItems.quantity;
          });
        } else {
          const newArr = this.getCookie("cart");
          this.arr = newArr;
          console.log(this.NumberItemsCookies);
          this.NumberItemsCookies.forEach((element) => {
            let boxProductItem = {
              orderFlavor: element[0],
              quantity: element[1],
            };
            this.orderItems.box_product.push(boxProductItem);
          });

          this.arr = [...this.arr, this.orderItems];
          document.cookie =
            "cart=" + JSON.stringify(this.arr) + ";domain=;path=/";
          console.log("no logged");
          carIconNavbar.numItemscarro += 1;
          this.totalQuantityCarItems += this.orderItems.quantity;
          this.orderItems.box_product = [];
          setTimeout(function () {
            alert("Se ha añadido el item al carrito!");
          }, 80);
        }
      } else {
        setTimeout(function () {
          alert(
            "No se puede añadir mas items al carro, el límite es de 6 productos por compra"
          );
        }, 60);
      }
    },
    /*
     *	Obtener el id pasado como query parmas,
     *	de la url de la pagina actual.
     */
    idDetails() {
      const search = window.location.search;
      const urlParam = new URLSearchParams(search);
      return parseInt(urlParam.get("id"));
    },
    /*
     *	Añade un nuevo atributo al objeto dbOrderItem,
     *	parametros de entrada una clave y valor del atributo
     */
    addDbOrderItem(key, value) {
      this.dbOrderItem = {
        ...this.dbOrderItem,
        [key]: value,
      };
    },
    /*
     *	Evento del button ir al carrito, añade el objeto dbOrderItem
     * al localStorage del navegador
     */
    handleGoCart() {
      LocalStorage.saveOrderItem(this.dbOrderItem);
    },
    changeImage(num) {
      this.imgPrincipal = num;
      // console.log(this.imgPrincipal);
    },

    calcularNumeroDeGalletas(arr) {
      return arr.map((i) => i[1]).reduce((a, b) => a + b);
    },
  },
});
