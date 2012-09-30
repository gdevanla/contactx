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
         $('#fullName').text(lp.firstName +'');
         $('#twitter').append('<li>'+ lp.lastName +'</li>');
         $('#twitter').append('<li>'+ lp.headline +'</li>');
         $('#twitter').append('<li>'+ lp.dateOfBirth.day +'</li>');
         $('#twitter').append('<li>'+ lp.dateOfBirth.month +'</li>');
         $('#twitter').append('<li>'+ lp.dateOfBirth.year +'</li>');
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
	
         $('#twitter').append('<li>'+ lp.industry +'</li>');
         $('#twitter').append('<li>'+ lp.interests +'</li>');
         $('#twitter').append('<li>'+ lp.mainAddress +'</li>');
         $('#twitter').append('<li><img src="'+ lp.pictureUrl +'"></li>');
	 $.each(lp.positions, function(i, item){
		$.each(item,function(h,k){
			//console.log(k);
			if (k.company){
        			$('#twitter').append('<li>company:'+ k.company.name +'</li>');
        			$('#twitter').append('<li>company:'+ k.company.industry +'</li>');
			}
			if (k.title){
        			$('#twitter').append('<li>title:'+ k.title +'</li>');
			}

		});
	 });
	 
         $('#twitter').append('<li>'+ lp.publicProfileUrl +'></li>');
	 $.each(lp.skills, function(i, item){
		$.each(item, function(h,k){
        		$('#twitter').append('<li>'+ k.skill.name +'</li>');
		});
	});
	
         $('#twitter').append('<li>'+ lp.specialties +'</li>');
   });
   



});


function displayEmployee(data) {
        var employee = data.item;
        console.log(employee);
        $('#employeePic').attr('src', 'pics/' + employee.picture);
        $('#fullName').text(employee.firstName + ' ' + employee.lastName);
        $('#employeeTitle').text(employee.title);
        $('#city').text(employee.city);
        console.log(employee.officePhone);
        if (employee.managerId>0) {
                $('#actionList').append('<li><a href="employeedetails.html?id=' + employee.managerId + '"><h3>View Manager</h3>' +
                                '<p>' + employee.managerFirstName + ' ' + employee.managerLastName + '</p></a></li>');
        }   
        if (employee.reportCount>0) {
                $('#actionList').append('<li><a href="reportlist.html?id=' + employee.id + '"><h3>View Direct Reports</h3>' +
                                '<p>' + employee.reportCount + '</p></a></li>');
        }   
        if (employee.email) {
                $('#actionList').append('<li><a href="mailto:' + employee.email + '"><h3>Email</h3>' +
                                '<p>' + employee.email + '</p></a></li>');
        }   
        if (employee.officePhone) {
                $('#actionList').append('<li><a href="tel:' + employee.officePhone + '"><h3>Call Office</h3>' +
                                '<p>' + employee.officePhone + '</p></a></li>');
        }   
        if (employee.cellPhone) {
                $('#actionList').append('<li><a href="tel:' + employee.cellPhone + '"><h3>Call Cell</h3>' +
                                '<p>' + employee.cellPhone + '</p></a></li>');
                $('#actionList').append('<li><a href="sms:' + employee.cellPhone + '"><h3>SMS</h3>' +
                                '<p>' + employee.cellPhone + '</p></a></li>');
        }   
        $('#actionList').listview('refresh');
     
}















