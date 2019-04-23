$(document).on('submit','#compilerform',function(e){
    e.preventDefault();
        var con=$.trim($("#code").val());
        console.log(con)
        var content = $('#code').html();
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        console.log(csrftoken)
        console.log(content)
        $.ajax ({
                url: "/pyExec/",
                type: "POST",
                dataType:'json',
                data: { 
                        'pyscript':con,       
                        'csrfmiddlewaretoken': csrftoken,
            },
                success:function(context){
                d=context.output
                $('#result').text(d);
                console.log(d)
                }
            
            
            });

})




