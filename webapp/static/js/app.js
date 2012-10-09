// The URL of the Singly API endpoint
var apiBaseUrl = 'https://api.singly.com';

// A small wrapper for getting data from the Singly API
var singly = {
   get: function(url, options, callback) {
      if (options === undefined ||
         options === null) {
         options = {};
      }

      options.access_token = accessToken;
      $.getJSON(apiBaseUrl + url, options, callback);
   }
};

// Runs after the page has loaded
$(function() {
   // If there was no access token defined then return
   if (accessToken === 'undefined' ||
      accessToken === undefined) {
      return;
   }

   singly.get('/services/linkedin/self',{}, function(data) {
	lp=data[0].data
         $('#employeePic').attr('src',lp.pictureUrl);
         $('#fullName').text(lp.firstName +' '+lp.lastName);
         $('#employeeTitle').text(lp.headline);
	 $('#city').text(lp.mainAddress);
	 //if (employee.email) {
                $('#actionList').append('<li><a href="mailto:freegyaan@gmail.com"><h3>Email</h3><p>freegyaan@gmail.com</p></a></li>');
         //}
	 $.each(lp.skills, function(i, item){
		$.each(item, function(h,k){
        		$('#skillset').append('<li>'+ k.skill.name +'</li>');
		});
	 });


         //$('#twitter').append('<li>'+ lp.dateOfBirth.day +'</li>');
         //$('#twitter').append('<li>'+ lp.dateOfBirth.month +'</li>');
        // $('#twitter').append('<li>'+ lp.dateOfBirth.year +'</li>');
	 $.each(lp.educations, function (i, item){
		$.each(item, function (h,k){
			if (k.fieldOfStudy){
        			$('#twitter').append('<li>'+ k.fieldOfStudy +'</li>');
			}
			if (k.schoolName){
        			$('#twitter').append('<li>'+ k.schoolName +'</li>');
			}

		});
	 });
	
         $('#coolstuff').append(lp.industry +', ');
         $('#coolstuff').append(lp.interests +', ');
         $('#coolstuff').append(lp.mainAddress +', ');
	 $.each(lp.positions, function(i, item){
		$.each(item,function(h,k){
			//console.log(k);
			if (k.company){
        			$('#coolstuff').append('<li>company:'+ k.company.name +'</li>');
        			$('#coolstuff').append('<li>company:'+ k.company.industry +'</li>');
			}
			if (k.title){
        			$('#coolstuff').append('<li>title:'+ k.title +'</li>');
			}

		});
	 });
	 
	
	
         $('#coolstuff').append('<li>'+ lp.specialties +'</li>');
   });
   



});
















