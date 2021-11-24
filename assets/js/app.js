function Download(url) {
    window.location.href = url 
  }
  
  
  (function() {
    const fn = function() {
      Bokeh.safely(function() {
        (function(root) {
          function embed_document(root) {
            
          const docs_json = document.getElementById('4915').textContent;
          const render_items = [{"docid":"c6c5b74b-8330-4b53-8cc5-a1814060c290","root_ids":["4308"],"roots":{"4308":"78be129b-ffc9-4187-a218-9863eb4e9e17"}}];
          root.Bokeh.embed.embed_items(docs_json, render_items);
        
          }
          if (root.Bokeh !== undefined) {
            embed_document(root);
          } else {
            let attempts = 0;
            const timer = setInterval(function(root) {
              if (root.Bokeh !== undefined) {
                clearInterval(timer);
                embed_document(root);
              } else {
                attempts++;
                if (attempts > 100) {
                  clearInterval(timer);
                  console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");
                }
              }
            }, 10, root)
          }
        })(window);
      });
    };
    if (document.readyState != "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  })();