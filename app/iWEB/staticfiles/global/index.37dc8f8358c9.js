var user = document.querySelector(".user");
var map = document.querySelector(".map");
var mapWidth = 1096;
var mapHeight = 1266;
createMaze({{maze|safe}});

// Converts from longitude and latitude to x and y coordinates
// The maths behind this function is explained in the documentation
function getCoordinates(lat, lng){
    // The coordinates of the top left and bottom right corners of the map
    var topLeft = {
        lat: 50.7390069,
        lng: -3.5379331
    }			
    var bottomRight = {
        lat: 50.7322172,
        lng: -3.52897
    }
    // Radius of the earth in km
    const radius = 6371; 

    // Calculates the coordinates for the top left and bottom right corners of the map
    topLeftX = radius*topLeft.lng*Math.cos((topLeft.lat + bottomRight.lat)/2);
    topLeftY = radius*topLeft.lat;
    bottomRightX = radius*bottomRight.lng*Math.cos((topLeft.lat + bottomRight.lat)/2);
    bottomRighty = radius*bottomRight.lat;

    // Calculates the coordinates for the input latitude and longitude
    posX = radius*lng*Math.cos((topLeft.lat + bottomRight.lat)/2);
    posY = radius*lat;

    // Calculates the percentage of the input latitude and longitude 
    // relative to the top left and bottom right corners of the map
    pos_perX = (posX - topLeftX )/(bottomRightX - topLeftX );
    pos_perY = (posY - topLeftY )/(bottomRighty  - topLeftY );

    return {
        x: 0 + (mapWidth - 0)*pos_perX+ "px",
        y: 0 + (mapHeight - 0)*pos_perY+ "px"
    }
    
}

// Get the user's location and sets the user's character to that location
function getLocation(track = false) {
    function success(position) {
        var latitude  = position.coords.latitude;
        var longitude = position.coords.longitude;
        var user = document.querySelector('.user');
        y = getCoordinates(latitude, longitude).y;
        x = getCoordinates(latitude, longitude).x;
        user.style.top = y;
        user.style.left = x;
    }
    function error() {
        throw new Error('Unable to retrieve your location');
    }
    // Options for geolocation
    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };
    // Check if geolocation is supported by the browser
    if (navigator.geolocation) {
        // If track is true, constantly update the user's location
        if (track) {
            watchID = navigator.geolocation.watchPosition(success, error, options)
            return watchID;
        } else {
            navigator.geolocation.getCurrentPosition(success, error, options);
        }
    } else {
        throw new Error('Geolocation is not supported by this browser.');
    }
}

// Represents the text file of the map as divs on the page
function createMaze(map) {
    // Removes all the previous maze divs if they exist
    var blocks = document.querySelectorAll('.maze-square');
    for (var i = 0; i < blocks.length; i++) {
        blocks[i].parentNode.removeChild(blocks[i]);
    }

    // Creates the maze divs
    var maze = map;
    for (var i = 0; i < maze.length; i++) {
        // Creates each row
        var row = maze[i];
        var maze_row = document.createElement('div');
        maze_row.setAttribute('class', 'maze-row');

        // Creates each square
        for (var j = 0; j < row.length; j++) {
            var square = row[j];
            var maze_square = document.createElement('div');			
            maze_square.setAttribute('class', 'maze-square');
            maze_square.setAttribute('id', i + '-' + j);
            // Sets the class of the square depending on whether it is a wall or a path
            // Allows for the search algorithm to work by differentiating between the walls and paths
            if (square == "#") {
                maze_square.setAttribute('class', 'maze-square wall');
            }else {
                maze_square.setAttribute('class', 'maze-square path');
            }
            maze_row.appendChild(maze_square);
        }
        document.querySelector('.map').appendChild(maze_row);
    }
}


// Creates the bottles on the map to represent the fountains
for (i in {{ fountain_locations|safe }}){
    var bottle = document.createElement("div");
    bottle.id = "bottle" + i;
    bottle.className = "bottle";
    map.appendChild(bottle);
    
    // Gets the x and y coordinates of the fountain
    var x = getCoordinates(({{ fountain_locations|safe }})[i][0], ({{ fountain_locations|safe }})[i][1]).x;
    var y = getCoordinates(({{ fountain_locations|safe }})[i][0], ({{ fountain_locations|safe }})[i][1]).y;

    // Retrieves extra information about the fountain from the database
    bottle.textContent = ({{ fountain_locations|safe }})[i][2] + " " + ({{ fountain_locations|safe }})[i][3];
    bottle.style.left = x;
    bottle.style.top = y;
    // Makes the bottle invisible
    bottle.style.display = "none";
    bottle.style.fontSize = "0px";

}

// Creates the bus stops on the map to represent the bus stops
for (i in {{ bus_stop_locations|safe}}){
    var bus_stop = document.createElement("div");
    bus_stop.id = "bus_stop" + i;
    bus_stop.className = "bus_stop";
    map.appendChild(bus_stop);
    
    // Gets the x and y coordinates of the bus stop
    var x = getCoordinates(({{ bus_stop_locations|safe }})[i][0], ({{ bus_stop_locations|safe }})[i][1]).x;
    var y = getCoordinates(({{ bus_stop_locations|safe}})[i][0], ({{ bus_stop_locations|safe }})[i][1]).y;

    // Retrieves extra information about the bus stop from the database
    bus_stop.textContent = ({{ bus_stop_locations|safe}})[i][2] + " " + ({{ bus_stop_locations|safe}})[i][3];
    bus_stop.style.left = x;
    bus_stop.style.top = y;

    // Makes the bus stop invisible
    bus_stop.style.display = "none";
    bus_stop.style.fontSize = "0px";

}

// Creates the bins on the map to represent the bins
for (i in {{ bin_locations|safe}}){
    var bin = document.createElement("div");
    bin.id = "bin" + i;
    bin.className = "bin";
    map.appendChild(bin);
    
    // Gets the x and y coordinates of the bin
    var x = getCoordinates(({{ bin_locations|safe}})[i][0], ({{ bin_locations|safe }})[i][1]).x;
    var y = getCoordinates(({{ bin_locations|safe}})[i][0], ({{ bin_locations|safe }})[i][1]).y;

    // Retrieves extra information about the bin from the database
    bin.textContent = ({{ bin_locations|safe }})[i][2] + " " + ({{ bin_locations|safe }})[i][3];
    bin.style.left = x;
    bin.style.top = y;

    // Makes the bin invisible
    bin.style.display = "none";
    bin.style.fontSize = "0px";

}

var bottles = document.querySelectorAll('.bottle');
var bus_stops = document.querySelectorAll('.bus_stop');
var bins = document.querySelectorAll('.bin');

// Checks to see if the user has clicked on a bottle
for (var i = 0; i < bottles.length; i++) {
    const x = bottle.offsetLeft;
    const y = bottle.offsetTop
    // When the user clicks on a bottle, a box appears with the information about the bottle
    bottles[i].addEventListener('click', createBox );

}

// Checks to see if the user has clicked on a bus stop
for (var i = 0; i < bus_stops.length; i++) {
    const x = bus_stop.offsetLeft;
    const y = bus_stop.offsetTop
    // When the user clicks on a bus stop, a box appears with the information about the bus stop
    bus_stops[i].addEventListener('click', createBox );

}

// Checks to see if the user has clicked on a bin
for (var i = 0; i < bins.length; i++) {
    const x = bin.offsetLeft;
    const y = bin.offsetTop
    // When the user clicks on a bin, a box appears with the information about the bin
    bins[i].addEventListener('click', createBox );

}

// Creates a button that displays the bottles when clicked and hides them when clicked again
var waterButton = document.querySelector('.water-fountain-button');
waterButton.addEventListener('click', function() {
    for (var i = 0; i < bottles.length; i++) {
        console.log(bottles[i].style.display);
        if (bottles[i].style.display == "none") {
            bottles[i].style.display = "block";
            waterButton.style.backgroundColor = "black";
        } else {
            bottles[i].style.display = "none";
            waterButton.style.backgroundColor = "blue";
        }
    }
});

// Creates a button that displays the bus stops when clicked and hides them when clicked again
var busButton = document.querySelector('.bus-stop-button');
busButton.addEventListener('click', function() {
    for (var i = 0; i < bus_stops.length; i++) {
        console.log(bus_stops[i].style.display);
        if (bus_stops[i].style.display == "none") {
            bus_stops[i].style.display = "block";
            busButton.style.backgroundColor = "black";
        } else {
            bus_stops[i].style.display = "none";
            busButton.style.backgroundColor = "red";
        }
    }
});

// Creates a button that displays the bins when clicked and hides them when clicked again
var binButton = document.querySelector('.bin-button');
binButton.addEventListener('click', function() {
    for (var i = 0; i < bins.length; i++) {
        console.log(bins[i].style.display);
        if (bins[i].style.display == "none") {
            bins[i].style.display = "block";
            binButton.style.backgroundColor = "black";
        } else {
            bins[i].style.display = "none";
            binButton.style.backgroundColor = "green";
        }
    }
});

// Creates a button that tracks the user's location
var trackButton = document.querySelector('.track-button');
trackButton.addEventListener('click', function() {
    if (trackButton.style.backgroundColor == "gray") {
        trackButton.style.backgroundColor = "white";
        trackButton.value = "Tracking: Off";
        navigator.geolocation.clearWatch(watchID)
    } else {
        trackButton.style.backgroundColor = "gray";
        trackButton.value = "Tracking: On";
        watchID = getLocation(track = true)
    }
});

// Checks if the user has completed the challange
function checkLocation(e){
    x = user.offsetLeft - this.Xcoordinates
    y = user.offsetTop - this.Ycoordinates
    console.log(x, y)
    if ( x < 10 && x > -10 && y < 10 && y > -10){
        alert("Congratulations! You have completed the challenge!");
    } else{
        alert("You are not at the correct location");
    }

}

// The function that creates the box with the information about the bottle, bus stop or bin
function createBox(e){
    var bottle_id = this.id;
    // Creates the first box that isn't interactive but contains the information about the bottle, bus stop or bin
    var box = document.createElement("div");
    box.id = "box";
    box.className = "box";
    box.style.left = this.style.left;
    box.style.top = this.style.top;
    box.innerHTML = this.textContent;
    // Changes the colour of the box depending on the type of object
    if (this.className == "bottle"){
        var color = "blue";
        var color_light = "#ADD8E6";
    } else if (this.className == "bus_stop"){
        var color = "red";
        var color_light = "pink";
    } else if (this.className == "bin"){
        var color = "green";
        var color_light = "lightgreen";
    }
    box.style.backgroundColor = color_light;

    // Adds the box to the map and displays it ontop of the bottle, bus stop or bin
    var map = document.querySelector('.map');
    map.appendChild(box);
    
    // Creates the second box that when clicked displays the shortest path to the bottle, bus stop or bin
    var pathButton = document.createElement("button");
    pathButton.id = "pathButton";
    pathButton.className = "pathButton";
    pathButton.style.left = '80px';
    pathButton.style.top = '100px';
    pathButton.innerHTML = "Find Shortest Path";
    pathButton.style.fontSize = "30px";
    pathButton.style.width = "280px";
    pathButton.style.height = "80px";
    pathButton.style.padding = '12px 24px';
    pathButton.style.color = '#fff';
    pathButton.style.backgroundColor = color;
    pathButton.style.borderRadius = '6px';
    pathButton.style.border = 'none';
    pathButton.style.cursor = 'pointer';

    //The coordinates to the bottle, bus stop or bin are stored in the pathButton
    pathButton.Xcoordinates = (this.offsetLeft);
    pathButton.Ycoordinates = (this.offsetTop);

    box.appendChild(pathButton);

    // Stops the box from being created multiple times
    this.removeEventListener('click', createBox);
    // When the path button is clicked the shortest path to the bottle, bus stop or bin is displayed
    pathButton.addEventListener('click', displayPath);

    // Creates a button that when pressed cheks to see if the user is at the bottle, bus stop or bin
    var checkButton = document.createElement("button");
    checkButton.id = "checkButton";
    checkButton.className = "checkButton";
    checkButton.style.left = '80px';
    checkButton.style.top = '200px';
    checkButton.innerHTML = "Veryify Location";
    checkButton.style.fontSize = "30px";
    checkButton.style.width = "280px";
    checkButton.style.height = "80px";
    checkButton.style.padding = '12px 24px';
    checkButton.style.color = '#fff';
    checkButton.style.backgroundColor = 'brown';
    checkButton.style.borderRadius = '6px';
    checkButton.style.border = 'none';
    checkButton.style.cursor = 'pointer';
    checkButton.Xcoordinates = (this.offsetLeft);
    checkButton.Ycoordinates = (this.offsetTop);
    box.appendChild(checkButton);

    // When the check button is pressed the user's location is checked
    checkButton.addEventListener('click', checkLocation);

    // Creates a red exit button that appears on the box and when pressed removes the box
    var exitButton = document.createElement("button");
    exitButton.id = "exitButton";
    exitButton.className = "exitButton";
    exitButton.style.left = '80px';
    exitButton.style.top = '100px';
    exitButton.innerHTML = "X";
    exitButton.style.cursor = 'pointer';
    exitButton.style.backgroundColor = "red";
    exitButton.style.fontSize = "30px";
    exitButton.style.width = "80px";
    exitButton.style.height = "80px";
    box.appendChild(exitButton);
    // When the exit button is pressed the box is removed
    exitButton.addEventListener('click', function() {
        // All of the boxes are removed
        pathButton.parentNode.removeChild(pathButton);
        this.parentNode.removeChild(this);
        box.parentNode.removeChild(box);

        // An event listener is added to the bottle, bus stop or bin so that the box can be created again
        var bottle = document.getElementById(bottle_id);
        bottle.addEventListener("click", createBox);		

        
    });
}

// A function that displays the shortest path from the user to the bottle, bus stop or bin
function displayPath (e){
    // Retrieves the coordinates of the user and converts them to the pixel equivilant
    var user = document.querySelector(".user");
    user_x = Math.floor(user.offsetLeft/18);
    user_y = Math.floor(user.offsetTop/18);
    
    // Retrieves the coordinates of the bottle, bus stop or bin and converts them to the pixel equivilant
    x = Math.floor(this.Xcoordinates/18);
    y = Math.floor(this.Ycoordinates/18);

    // Runs the A* algorithm to find the shortest path
    maze = {{ maze|safe }};
    var path = aStar(maze, [user_y, user_x], [y,x]);

    // Displays the path on the map by chaning the background colour of the divs
    createPath(path, this.style.backgroundColor);
    createMaze(maze);

}

// A function that recieves the dictioniary of the shortest path and then turns the indexes into the correct coordinates and creates divs to represent the path
function createPath(path, color){

    // Removes the previous path
    var blocks = document.querySelectorAll('.pathDiv');
    for (var i = 0; i < blocks.length; i++) {
        blocks[i].parentNode.removeChild(blocks[i]);
    }
    for (i in path){
        var pathDiv = document.createElement("div");
        pathDiv.id = "path" + i;
        pathDiv.className = "pathDiv";
        pathDiv.style.backgroundColor = color;
        pathDiv.style.opacity = "0.8";
        
        pathDiv.style.left = ('' + path[i][1]*18 + 'px');
        pathDiv.style.top = ('' + path[i][0]*18 + 'px');
        map.appendChild(pathDiv);

    }
}

// This represents each node in the grid for the A* algorithm
class Node {
    constructor(parent = null,position) {
        this.position = position;
        this.parent = parent;
        this.g = 0; // The shortes distance from the start node to the current node
        this.h = 0; // An estimate of the distance to the end node
        this.f = 0; // The sum of the g and h values
    }

    isEqual(other) {
        return this.position == other.position;
    }
}

// This function runs the A* algorithm to find the shortest path
// It takes in the maze, the start and end coordinates and returns the shortest path
// The A* algorithm is explained better in the documentation
// The code for the A* algorithm was adapted from psuedo code from https://en.wikipedia.org/wiki/A*_search_algorithm
function aStar(map, start, end){
    
    // Creates the start and end node representations of the arguments passed in
    var start = new Node(null,start);
    start.g = start.f = start.h = 0;
    var end = new Node(null,end);
    end.g = end.f = end.h = 0;
    
    // The list of nodes that have been and haven't visited
    var openList = [];
    var closedList = [];

    // Possible ways the node can move in
    var positions = [
    [0, -1],
    [0, 1],
    [-1, 0],
    [1, 0],
    [-1, -1],];

    openList.push(start);

    // Loops until the end is found or openList is empty
    while(openList.length > 0){
        
        var currentNode = openList[0];
        var currentIndex = 0;
        for (var index in openList) {
            // Finds the node with the lowest f value in the openList(nodes that aren't discarded)
            // Sets the current node to that node
            if (openList[index].f < currentNode.f) {
                currentNode = openList[index];
                currentIndex = index;
            }
        }
        // Removes the current node from the openList and adds it to the closedList(nodes that have been visited)
        openList.splice(currentIndex, 1);
        closedList.push(currentNode);

        // If the current node is the end node then the path is found
        if(currentNode.position[0] == end.position[0] && currentNode.position[1] == end.position[1]){
                
            var path = [];
            var current = currentNode;
            
            // Gets the positions of the nodes in the path
            while(current != null){
                path.push(current.position);
                current = current.parent;
            }
            return path.reverse();
        }

        var children = [];

        for (var newPosition of positions){
            var nodePosition = [
                currentNode.position[0] + newPosition[0],
                currentNode.position[1] + newPosition[1]
                
            ];

            // Checks if the node is in the map
            if(nodePosition[0] > (map.length - 1) || nodePosition[0] < 0 || nodePosition[1] > (map.length - 1) || nodePosition[1] < 0){
                continue;
            }
            // Checks if the node is a wall
            if(map[nodePosition[0]][nodePosition[1]] != '-'){
                continue;
            }

            // Create a new child node
            var newNode = new Node(currentNode,nodePosition);
            children.push(newNode);
        }

        // Looks thorugh the childer nodes
        for(var child of children){
            // Makes sure the child node isn't in the closedList
            for(var closedChild of closedList){
                if(child.isEqual(closedChild)){
                    continue;
                }
            }

            // Adds the weight of the path from hte child node to the current node in our case it is 1 since every distance is the same
            child.g = currentNode.g + 1;
            // Calculates the heuristic value using uclidean distance
            // TODO: Try different heuristics
            child.h = Math.pow((child.position[0] - end.position[0]), 2) + Math.pow((child.position[1] - end.position[1]), 2);          
            child.f = child.g + child.h;

            // Check to see if the child node is not further away from the end node than nodes in the openList
            for(var openNode in openList){
                if(child.isEqual(openNode) && child.g > openNode.g){
                    continue;
                }
            }

            // Adds the child node to the openList
            openList.push(child);
            // Sets the child node to a wall for memory efficiency
            // However makes the path less accurate but since the path is only used for visualisation it doesn't matter
            // TODO: Try to find a way to make the path more accurate
            maze[child.position[0]][child.position[1]] = "#";
        }
    }
}