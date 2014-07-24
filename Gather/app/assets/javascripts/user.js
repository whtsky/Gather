
user = {
	login: function(){
		$.get("/get_pk", function(d){
			pk = eval(d);
			key = new RSAKey();
			key.setPublic(pk[1],pk[0]);
			$("#login-form").submit(function(e){
				e.preventDefault();
				
				
				var data = $("#login-form").serializeArray();
				console.log(key.encrypt("miao"));
	  		});
		});

	},
	signup: function(){
	
	}
}