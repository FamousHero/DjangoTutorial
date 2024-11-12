console.log("Hello world!");

$(document).ready(function(){
    const buttons = $('button');
    const table = $('table');
    const csrf_token = $("input[name='csrfmiddlewaretoken']").val()
    
    if(table){
        if(table.attr('aria-label') == 'Device Info'){
            buttons.each(function(){
                const button = $(this);
                const table_row = button.parent().parent();
                const mac_address = table_row.children().eq(1).text();
                
                button.click(async ()=>{
                    try{
                        const relative_url = mac_address+'/delete';
                        const response = await fetch(relative_url,{
                            method: "DELETE",
                            headers: {
                                'X-CSRFToken': csrf_token
                            },
                        })
                        if(!response.ok){
                            throw new Error('not ok');
                        }
                    } catch(error){
                        console.error(error.message);
                    }
                })
            })
        }
        else if(table.attr('aria-label') == 'Cable Info'){
            buttons.each(function(){
                const button = $(this);
                const table_row = button.parent().parent();
                const pk = table_row.children().eq(0).text();
                
                button.click(async ()=>{
                    try{
                        const relative_url = pk+'/delete';
                        const response = await fetch(relative_url,{
                            method: "DELETE",
                            headers: {
                                'X-CSRFToken': csrf_token
                            },
                        })
                        if(!response.ok){
                            throw new Error('not ok');
                        }
                        table_row.remove();
                    } catch(error){
                        console.error(error.message);
                    }
                })
            })
        }
    }
}
)