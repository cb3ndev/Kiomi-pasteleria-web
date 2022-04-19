class LocalStorage {
	/* 
		Guardar un item en el localStorage
	*/
	static saveOrderItem (item) {
		localStorage.setItem('order', JSON.stringify(item))
	}
	/* 
		Obtener un item del localStorage
	*/
	static getOrderItem () {
		return JSON.parse(localStorage.getItem('trip'))
	}
	/* 
		Eliminar el item del localStorage
	*/
	static deleteOrderItem () {
		localStorage.removeItem('order')
	}
}

export {
	LocalStorage
}