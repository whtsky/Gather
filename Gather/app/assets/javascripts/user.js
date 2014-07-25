

user = {
	login: function(){
		$("#login-form").submit(function(e){
			e.preventDefault();
			b64 = new Base64()
			data = b64.encode($("#login-form").serializeArray());
			$.post("/sign", {encrypted_json: data},function(result){
				console.log(result);
			});
  		});

	},
	signup: function(){
	
	}
}