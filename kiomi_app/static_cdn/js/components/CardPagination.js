//import api from "../api"

Vue.component('card-pagination', {
	name: 'card-pagination',
	props: {
		totalPages: {
			type: Number,
		},
		currentPage:{
			type: Number,
		},	
	},
	computed: {
		dividir: function () {
		  // `this` points to the vm instance
		 const arr = this.totalPages
		  return arr
		}
	
	},
	template: /*html*/`
	<nav aria-label="Page navigation example">
	<ul class="pagination justify-content-center">
		<li class="page-item" >
			<a class="page-link" tabindex="-1" aria-disabled="true" @click="loadPrev()" >Previous</a>
		</li>
		<li class="page-item" v-for= "i in dividir">
			<a class="page-item page-link" @click="currentPage--">{{i}}</a>
		</li>
		<li class="page-item">
			<a class="page-link" @click="loadNext()">Next</a>
		</li>
	</ul>
	</nav>
	`
})