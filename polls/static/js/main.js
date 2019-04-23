$(document).ready(function(){

	// -----------------------------------counter for timer------------------------
    var test_counter = 0;
    setInterval(function () {
        console.log("hi");
        test_counter++;
        document.getElementById('timer').value=test_counter;
  
    },1000);

    // -----------------------------------------------------------------------------
    var testSubmit = $("#testSubmitBtn").click(function(){
        var data = $("#test").serializeArray()
        var posting = $.post( '/testcal/', { 's': data} );
    })
 
    locations = [
        {
        "id":0,
        "text": "Andhra Pradesh",
        },
        {
        "id":1,
        "text": "Arunachal Pradesh",
        },
        {
        "id":2,
        "text": "Bihar",
        },
        {
        "id":3,
        "text": "Chhattisgarh",
        },
        {
        "id":4,
        "text": "Goa",
        },
        {
        "id":5,
        "text": "Gujarat",
        },
        {
        "id":6,
        "text": "Haryana",
        },
        {
        "id":7,
        "text": "Jammu and Kashmir",
        },
        {
        "id":8,
        "text": "Jharkhand",
        },
        {
        "id":9,
        "text": "Karnataka",
        },
        {
        "id":10,
        "text": "Kerala",
        },
        {
        "id":11,
        "text": "Madhya Pradesh",
        },
        {
        "id":12,
        "text": "Maharashtra",
        },
        {
        "id":13,
        "text": "Manipur",
        },
        {
        "id":14,
        "text": "Meghalaya",
        },
        {
        "id":15,
        "text": "Mizoram",
        },
        {
        "id":16,
        "text": "Nagaland",
        },
        {
        "id":17,
        "text": "Odisha",
        },
        {
        "id":18,
        "text": "Punjab",
        },
        {
        "id":19,
        "text": "Rajasthan",
        },
        {
        "id":20,
        "text": "Sikkim",
        },
        {
        "id":21,
        "text": "Tamil Nadu",
        },
        {
        "id":22,
        "text": "Telangana",
        },
        {
        "id":23,
        "text": "Tripura",
        },
        {
        "id":24,
        "text": "Uttarakhand",
        },
        {
        "id":25,
        "text": "Uttar Pradesh",
        },
        {
        "id":26,
        "text": "West Bengal",
        },
        {
        "id":27,
        "text": "Andaman and Nicobar Island",
        },
        {
        "id":28,
        "text": "Chandigarh",
        },
        {
        "id":29,
        "text": "Dadra and Nagar Haveli",
        },
        {
        "id":30,
        "text": "Daman and Diu",
        },
        {
        "id":31,
        "text": "Delhi",
        },
        {
        "id":32,
        "text": "Lakshadweep",
        },
        {
        "id":33,
        "text": "Puducherry",
        }





]
       

        // # "Telangana": "Telangana",
        // # "Tripura": "Tripura",
        // # "Uttarakhand": "Uttarakhand",
        // # "Uttar Pradesh": "Uttar Pradesh",
        // # "West Bengal": "West Bengal",
        // # "Andaman and Nicobar Island": "Andaman and Nicobar Island",
        // # "Chandigarh": "Chandigarh",
        // # "Dadra and Nagar Haveli": "Dadra and Nagar Haveli",
        // # "Daman and Diu": "Daman and Diu",
        // # "Delhi": "Delhi",
        // # "Lakshadweep": "Lakshadweep",
        // # "Puducherry": "Puducherry",
      occupation=[
        {
        "id":0,
        "text": "Student",
        },
        {
        "id":1,
        "text": "Employee",
        }]
      $("#occupation").select2(
      {
        data:occupation
      })  
      $("#locations").select2(
      {
        data: locations
    })

      $("section").click(function(e){
        a = e.target.closest("section")
        a.attr('id')
    });

      $("a[name='Messages']").click(function (e) {
        $.ajax({
        type: "GET",
        url:"/message",
        success: function(data){
           console.log(data)

        }
    });
});

// $("#compilerSelect").on('change', function() {
//   alert( this.value );
// });

 // $("#compiler").click(function(){
 //     var to_compile = {
 //                "LanguageChoice": $("#compilerSelect").val(),
 //                "Program": $("#code").val(),
 //                "Input": "",
 //                "CompilerArgs" : ""
 //            };
 //     $.ajax ({
 //            url: "http://rextester.com/rundotnet/api",
 //            type: "POST",
 //            data: to_compile
 //        }).done(function(data) {
 //            $("#programErr").html(data["Errors"])
 //            $("#programRe").html(data["Result"])
 //            $("#programStats").html(data["Stats"])
 //        }).fail(function(data, err) {
 //        });
 // })



    // a = $("#course")
    // a.change(function() {$.ajax({
    //     type:"GET",
    //     url: "http://127.0.0.1:8000/courseAjax/" + $("#course").val(),
    //     success : function(response) {
    //         $("#chapt").select2({
    //           data:response.chapters
    //         })
    //     },
    //     error: function() {
    //         alert('Error occured');
    //     }
    // });
    // });



   
