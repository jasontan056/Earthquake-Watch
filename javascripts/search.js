/**
 * obtain the name of the location from Google Map API's address object
 * @param[IN]: Google Map API's address object
 * @return the name of the location
 */
function getLocationName(addrObj)
{
    var name = "";
    var addrComponents = addrObj.address_components;
    for(var j = 0; j < addrObj.address_components.length; j++)
    {
        var curSubName = addrComponents[j].long_name;
        if(j == 0)
            name +=  curSubName + ", ";
        else
        {
            // avoid duplicate names such as "Los Angeles, Los Angeles, California, United States"
            var prevSubName = addrComponents[j - 1].long_name;
            if(curSubName != prevSubName)
            name += curSubName + ", ";
        }
    }

    // remove trailing ", "
    name = name.substring(0,name.length-2);
    return name; 
}

/**
 * display status message of search result such as "Did you mean?" and "Sorry no result found for <input>..."
 * @param[IN] the type of status, true for good result, false for no result
 * @param[IN] the msg the user wants to display
 * @out display the status message on the browser
 */
function displayStatus(type, msg)
{
    var result = document.createElement("b");	result.id = "result";

    if(type == true)
        result.innerHTML = "Did you mean?";
    else
        result.innerHTML = "Sorry, no result found for " + msg +"...";
   
    document.body.appendChild(result);
}

/**
 * obtain the user input in "searchbox" input box.
 * use Google Map API's geocode to obtain a list of possible matches of the user input
 * if the list is not empty, display "Did you mean?" followed by a list of the names of the locations 
 * other wise, display "Sorry, no result found for <user input>..."
 */
function codeAddress()
{	
    //create the Google Geocoder object.
    var geocoder = new google.maps.Geocoder();
    
    // address is the user input in the search box.
    var address = document.getElementById("searchbox").value;
    
    // create a unordered list.
    var choices = document.createElement("ul")
    choices.id = "choices";

    // search for the locations using Google Map API's geocode function.
    geocoder.geocode( { 'address': address}, function(results, status)
    {
        // if any result is found.
        if (status == google.maps.GeocoderStatus.OK)
        {
            // display "Did you mean?"
            displayStatus(true,"");
            // for each result
            for(var i = 0; i < results.length; i++)
            {				
                // Obtain the name of the location.				
                var locationName = getLocationName(results[i]);
    
                // create an "a" element and append the location's name.
                var a = document.createElement("a");
                a.innerHTML = locationName;

                // include the name information and location information in the "a" element.
                var coords = results[i].geometry.location.toString();
                a.href = coords.substring(1, coords.length - 1);
                a.value = locationName;
    
                // create a "li" element for "ul".
                var li = document.createElement("li");
                li.appendChild(a);
                choices.appendChild(li);
    
                // display the list on the browser
                document.body.appendChild(choices);
            }
        }
        
        // if the user's location is non sense to Google Map API.
        else
            displayStatus(false, address);
    });
}
    
/**
 * remove the old result status line, and the list of possible matches
 * then display the new result status and new list of possible matches
 */
function respondToInput()
{	
    $("#result").remove();
    $("#choices").remove();
    
    codeAddress();
}
    
/**
 * get the value corresponding to varialeName in the cookie string
 *@param[IN] the name of the variable
 *@return the value of that variable
 */
function getCookieValue(variableName)
{
    // cookiStr is in the form: name="value"
    var cookieStr = document.cookie;
    
    // check if the variable already exists
    var variablePos = cookieStr.search(variableName + "=");
    
    if(variablePos == -1)
        return "";
    
    // get the position of the char after ="
    var start = variablePos + variableName.length + 1 + 1;
    var end;

    for(end = start; end < cookieStr.length; end++)
        if (cookieStr[end] == "\"")
            break;
    
    return cookieStr.substring(start, end);
}
    
/**
 * display the message "You are watching <location name>."
 *@param[IN] the name of the location
 *@display the message "You are watching <location name>."
 */
function displayCurrentRegion(regionName, coords)
{
    // delete old you-are-watching message
    $("#watching").remove();
    $("#region").remove();
    $("#result").remove();
    $("#choices").remove();
    
    // add new you-are-watching message
    var watching = document.createElement("b");
    var region = document.createElement("a");
    watching.id = "watching";
    region.id = "region";
    
    watching.innerHTML = "You are watching ";
    region.innerHTML = regionName + ".<br/><br/>";
    
    if(coords != "")
    region.href = coords;
    
    document.body.appendChild(watching);
    document.body.appendChild(region);
}
