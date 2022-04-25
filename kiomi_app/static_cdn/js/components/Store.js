// import StoreCardProduct from './StoreCardProduct'
//  const currentPage= 1;

import api from "../api.js";
new Vue({
  delimiters: ["[[", "]]"],
  el: "#store",
  data() {
    return {
      dbProducts: [],
      currentPage: 1,
      totalPages:1,
      arrPages:[],
      showNextButton: false,
      showPrevButton: false,
    }
  },

  created() {   
    api
    .getProducts(this.currentPage)
    .then((products) => {
      this.dbProducts = products.results
      
      const numero = Math.ceil((products.count)/2);
      this.totalPages = numero
      
      const arr = []
      for (let i = 0; i<numero; i++) {
        arr[i]=i+1; 
      }
      this.arrPages = arr
      

      this.showNextButton = false
      this.showPrevButton = false
      if (products.next) {
        this.showNextButton = true
      }

      if (products.previous) {
        this.showPrevButton = true
    
      }
    })   
  },
  methods: {
    loadNext() {
      this.currentPage += 1
      api.getProducts(this.currentPage)
      .then((products) => {
        this.dbProducts = products.results})
    },
    loadPrev() {
      this.currentPage -= 1
      api.getProducts(this.currentPage)
      .then((products) => {
        this.dbProducts = products.results})
    },
    loadCurrentPage(page){
      this.currentPage = page
      api.getProducts(this.currentPage)
      .then((products) => {
        this.dbProducts = products.results})
    }
  },
});
