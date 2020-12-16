/*
Below is the original javascript before obfuscation using google ClosureCompiler

Use these to debug/tweak the footer behavior when needed, run the final code
through http://closure-compiler.appspot.com/home to obfuscate it before release
to generate_versions.js

Siming Yuan <siyuan@cisco.com>
------------------------------------------------------------------------------*/
var versions;       //all available versions
var version_table = $('<dl><dt>Versions</dt></dl>'); //version table
var version_pattern = /\/(?:latest|v[0-9]+\.[0-9]+\.[0-9]+)\//
var path = window.location.pathname; //browser pathname
var docroot = path.substring(0, path.search(version_pattern) + 1)

// find all latest versions
$.ajax({
    url: docroot,   // always look in doc root for versions
    success: function(data){
        // find all with version string
        // latest goes first, then add the releases, sorted reversed
        var latest = $(data).find("a:contains(latest)");
        var releases = $(data).find("a:contains(v)");
        versions = releases.add(latest).get().reverse();

        // generate entry in versions section
        $(versions).each(function(){

            // new version directory
            //get rid of training '/''
            var name = $(this).text();
            name = name.substring(0, name.length-1)

            // create new version html
            // compute target href based on current path
            var version = $('<dd></dd>').html($('<a>',{
                text: name,
                href: path.replace(version_pattern, "/" + name + "/"),
            }));

            // this is our current version
            if (path.indexOf("documentation/" + name + "/") >= 0) {
                version = $('<strong></strong>').html(version);

                // flag the version string dropdown
                $('span.version_name').first().html("v: " + name)

                //add the pdf link
                $('<dl>' +
                    '<dt>Download</dt>' +
                    '<dd>' + 
                        '<a href="' + 
                            docroot + $(this).attr("href") + 
                            'pyATS.pdf">PDF</a>' +
                    '</dd>' +
                  '</dl>').insertAfter('.version_table');
            }
            
            // add this version to version block
            version.appendTo(version_table);
        });

        //add version block to document
        $(".version_table").html(version_table)
     }
});
