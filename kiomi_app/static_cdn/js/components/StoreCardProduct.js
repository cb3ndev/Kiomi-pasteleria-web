const url = "http://127.0.0.1:8000/api";
Vue.component("store-card-product", {
  name: "store-card-product",
  props: {
    product: {
      type: Object,
      default: () => {},
    },
  },
  template: /*html*/ `
	<div class="card-product col-sm-12 col-md-6 col-lg-4 ">
		<div class="card">
			<img :src="product.image_1" class="card-img-top" :alt="product.name">
      <div class="card-body">
 		    <h5 class="card-title font-georgia-italic font-weight-bold">{{ product.name }}</h5>
  		  
  		  <a :href="'/product-details/?id='+product.id" class="btn btn-primary font-stem-bold">Comprar</a>
  		</div>
		</div>
	</div>
	`,
});
