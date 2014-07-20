
user = {
	login: function(){
		$.get("/get_pk", '', function(data){
			kp = eval(data);
			console.log(new RSAPublicKey(data[1], data[0]));
		});
	},
	signup: function(){
	
	}
}