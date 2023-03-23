var map
var mapWidth = 1096;
var mapHeight = 1266;
var watchID;

// Converts from longitude and latitude to x and y coordinates
// The maths behind this function is explained in the documentation
function getCoordinates(lat, lng, map_width = mapWidth, map_height = mapHeight){
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
    var topLeftX = radius*topLeft.lng*Math.cos((topLeft.lat + bottomRight.lat)/2);
    var topLeftY = radius*topLeft.lat;
    var bottomRightX = radius*bottomRight.lng*Math.cos((topLeft.lat + bottomRight.lat)/2);
    var bottomRighty = radius*bottomRight.lat;

    // Calculates the coordinates for the input latitude and longitude
    var posX = radius*lng*Math.cos((topLeft.lat + bottomRight.lat)/2);
    var posY = radius*lat;

    // Calculates the percentage of the input latitude and longitude 
    // relative to the top left and bottom right corners of the map
    var pos_perX = (posX - topLeftX )/(bottomRightX - topLeftX );
    var pos_perY = (posY - topLeftY )/(bottomRighty  - topLeftY );
    
    return {
        x: 0 + (map_width - 0)*pos_perX+ "px",
        y: 0 + (map_height - 0)*pos_perY+ "px"
    }
    
}


function createElement(index, data, className) {
    const map = document.querySelector(".map");
    const element = document.createElement("div");
    element.id = `${className}-${index}`;
    element.className = className;
  
    const { x, y } = getCoordinates(data[0], data[1], map.offsetWidth, map.offsetHeight);
  
    element.latitude = data[0];
    element.longitude = data[1];
    element.textContent = `${data[2]} ${data[3]}`;
    element.style.left = x;
    element.style.top = y;
    element.style.display = "none";
    element.style.fontSize = "0px";
  
    return element;
  }
  
function createItems(itemData, className) {
    const map = document.querySelector(".map");
  
    itemData.forEach((data, index) => {
      const element = createElement(index, data, className);
      map.appendChild(element);
    });
  }


  function getLocation(track = false, askPermission = true) {
    var map = document.querySelector(".map");
    var mapWidth = map.offsetWidth;
    var mapHeight = map.offsetHeight;
  
    function success(position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;
  
      var user = document.querySelector('.user');
      user.longitude = longitude;
      user.latitude = latitude;
      user.style.top = getCoordinates(latitude, longitude, mapWidth, mapHeight).y;
      user.style.left = getCoordinates(latitude, longitude, mapWidth, mapHeight).x;
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
  
    if (askPermission) {
      // Prompt the user for permission to access their location
      navigator.permissions.query({name: 'geolocation'}).then(function(result) {
        if (result.state === 'granted') {
          // If permission is granted, get the user's location
          if (track) {
            return navigator.geolocation.watchPosition(success, error, options);
          } else {
            navigator.geolocation.getCurrentPosition(success, error, options);
          }
        } else if (result.state === 'prompt') {
          // If permission is not granted but the user can be prompted, show a prompt
          navigator.geolocation.getCurrentPosition(success, error, options);
        } else {
          // If permission is denied, throw an error
          throw new Error('Geolocation permission denied.');
        }
      });
    } else {
      // If permission is not required, get the user's location
      if (track) {
        return navigator.geolocation.watchPosition(success, error, options);
      } else {
        navigator.geolocation.getCurrentPosition(success, error, options);
      }
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


function startListeners(maze_array) {
    var bottles = document.querySelectorAll('.bottle');
    var bus_stops = document.querySelectorAll('.bus_stop');
    var bins = document.querySelectorAll('.bin');

        // Checks to see if the user has clicked on a bottle
        for (var i = 0; i < bottles.length; i++) {

        // When the user clicks on a bottle, a box appears with the information about the bottle
        bottles[i].addEventListener('click', function() {
            createBox.call(this, maze_array); // Invoke createBox with 'this' set to the clicked bottle
        });
    
    }
    

    // Checks to see if the user has clicked on a bus stop
    for (var i = 0; i < bus_stops.length; i++) {
        // When the user clicks on a bottle, a box appears with the information about the bottle
        bus_stops[i].addEventListener('click', function() {
            createBox.call(this, maze_array); // Invoke createBox with 'this' set to the clicked bottle
        });
    }

    // Checks to see if the user has clicked on a bin
    for (var i = 0; i < bins.length; i++) {

        // When the user clicks on a bottle, a box appears with the information about the bottle
        bins[i].addEventListener('click', function() {
            createBox.call(this, maze_array); // Invoke createBox with 'this' set to the clicked bottle
        });
    }
    // Creates a button that displays the bottles when clicked and hides them when clicked again
    var waterButton = document.querySelector('.water-fountain-button');
    waterButton.addEventListener('click', function () {
        
        for (var i = 0; i < bottles.length; i++) {
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
            watchID = getLocation(true)
        }
    });
}


// The function that creates the box with the information about the bottle, bus stop or bin
function createBox(map_array){

    var bottle_id = this.id;
    // Creates the first box that isn't interactive but contains the information about the bottle, bus stop or bin
    var box = document.createElement("div");
    box.id = "info-box";
    box.className = "info-box";
    box.style.left = this.style.left;
    box.style.top = this.style.top;
    box.innerHTML = this.textContent;
    // Stores the id of the bottle, bus stop or bin in the box
    box.item_id = this.id;

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
    pathButton.style.position = 'absolute';
    pathButton.id = "pathButton";
    pathButton.className = "pathButton";
    pathButton.innerHTML = "Find Shortest Path";
    pathButton.style.fontSize = "10px";
    pathButton.style.width = "60px";
    pathButton.style.height = "60px";
    pathButton.style.color = '#fff';
    pathButton.style.backgroundColor = color;
    pathButton.style.borderRadius = '6px';
    pathButton.style.border = 'none';
    pathButton.style.cursor = 'pointer';
    pathButton.style.marginTop = '30px';
    pathButton.style.left = '0%';
    pathButton.style.top = '35px';

    //The coordinates to the bottle, bus stop or bin are stored in the pathButton
    pathButton.Xcoordinates = (this.offsetLeft);
    pathButton.Ycoordinates = (this.offsetTop);

    box.appendChild(pathButton);

    // Stops the box from being created multiple times
    this.removeEventListener('click', createBox);
    // When the path button is clicked the shortest path to the bottle, bus stop or bin is displayed
    pathButton.addEventListener('click', function(){
        displayPath.call(this, map_array);
    });

    // Creates a button that when pressed cheks to see if the user is at the bottle, bus stop or bin
    var checkButton = document.createElement("button");
    checkButton.id = "checkButton";
    checkButton.className = "checkButton";
    checkButton.style.position = 'absolute';
    checkButton.style.left = '0px';
    checkButton.style.top = '120px';
    checkButton.innerHTML = "Veryify Location";
    checkButton.style.fontSize = "10px";
    checkButton.style.width = "60px";
    checkButton.style.height = "60px";
    checkButton.style.color = '#fff';
    checkButton.style.backgroundColor = 'brown';
    checkButton.style.borderRadius = '6px';
    checkButton.style.border = 'none';
    checkButton.style.cursor = 'pointer';
    checkButton.style.marginTop = "10px";
    checkButton.Xcoordinates = (this.offsetLeft);
    checkButton.Ycoordinates = (this.offsetTop);
    checkButton.type_used = document.getElementById(bottle_id).className;
    box.appendChild(checkButton);

    // When the check button is pressed the user's location is checked
    checkButton.addEventListener('click', checkLocation);

    // Creates a red exit button that appears on the box and when pressed removes the box
    var exitButton = document.createElement("button");
    exitButton.id = "exitButton";
    exitButton.style.position = 'absolute';
    exitButton.className = "exitButton";
    exitButton.style.left = '0px';
    exitButton.style.top = '185px';
    exitButton.innerHTML = "X";
    exitButton.style.cursor = 'pointer';
    exitButton.style.backgroundColor = "red";
    exitButton.style.fontSize = "30px";
    exitButton.style.width = "60px";
    exitButton.style.height = "60px";
    exitButton.style.borderRadius = "6px";
    // Sets the exit button's top margin to 10px
    exitButton.style.marginTop = "10px";
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
function displayPath (map_array){
        // Retrieves the coordinates of the user and converts them to the pixel equivilant
        var user = document.querySelector(".user");


        var user_coordinates = getCoordinates(
            user.latitude,
            user.longitude);
        // removes the px from the end of the string
        var user_coordinates_x = user_coordinates.x.slice(0, -2);
        var user_coordinates_y = user_coordinates.y.slice(0, -2);

        var user_x = Math.floor(user_coordinates_x/18);
        var user_y = Math.floor(user_coordinates_y/18);

        // Retrieves the id of the bottle, bus stop or bin
        var item_id = this.parentElement.item_id;
        // Retrieves the item from the id of the bottle, bus stop or bin
        var item = document.getElementById(item_id);
        var item_coordinates = getCoordinates(
            item.latitude,
            item.longitude);

        // removes the px from the end of the string
        var item_coordinates_x = item_coordinates.x.slice(0, -2);
        var item_coordinates_y = item_coordinates.y.slice(0, -2);


        // Retrieves the coordinates of the bottle, bus stop or bin and converts them to the pixel equivilant
        var x = Math.floor(item_coordinates_x/18);
        var y = Math.floor(item_coordinates_y/18);

        // Runs the A* algorithm to find the shortest path
        var path = aStar(map_array, [user_y, user_x], [y,x]);
        
        // Displays the path on the map by chaning the background colour of the divs
        createPath(path, this.style.backgroundColor);
        createMaze(map_array);

}

// A function that recieves the dictioniary of the shortest path and then turns the indexes into the correct coordinates and creates divs to represent the path
function createPath(path, color){
    const map = document.querySelector(".map");
    var width_ratio = map.offsetWidth / 1096;
    var height_ratio = map.offsetHeight / 1266;
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
        
        pathDiv.style.left = ('' + width_ratio*path[i][1]*18 + 'px');
        pathDiv.style.top = ('' + height_ratio*path[i][0]*18 + 'px');
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
function aStar(maze, start, end){
    // Creates a deep copy of the maze to prevent modifying the original maze
    var mazeGrid = maze.map(row => row.slice());

    // Creates the start and end node representations of the arguments passed in
    var startNode = new Node(null, start);
    startNode.g = startNode.f = startNode.h = 0;
    var endNode = new Node(null, end);
    endNode.g = endNode.f = endNode.h = 0;

    
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

    openList.push(startNode);

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
        if(currentNode.position[0] == endNode.position[0] && currentNode.position[1] == endNode.position[1]){
                
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
            if(nodePosition[0] > (mazeGrid.length - 1) || nodePosition[0] < 0 || nodePosition[1] > (mazeGrid.length - 1) || nodePosition[1] < 0){
                continue;
            }
        
            // Checks if the node is a wall
            if(mazeGrid[nodePosition[0]][nodePosition[1]] != '-'){
                
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
            child.h = Math.pow((child.position[0] - endNode.position[0]), 2) + Math.pow((child.position[1] - endNode.position[1]), 2);          
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
            mazeGrid[child.position[0]][child.position[1]] = "#";
        }
    }
}


// Checks if the user has completed the challange
function checkLocation(e){
    const user = document.querySelector(".user");
    let x = user.offsetLeft - this.Xcoordinates
    let y = user.offsetTop - this.Ycoordinates
    if ( x < 10 && x > -10 && y < 10 && y > -10){
        // Creates a POST request to the server to update the database
        var csrftoken = getCookie('csrftoken');

        var request = new XMLHttpRequest();
        request.open("POST", "/index", true);
        request.setRequestHeader("Content-Type", "application/json");
        request.setRequestHeader("X-CSRFToken", csrftoken);
        request.send(JSON.stringify({points: 250, type_used : this.type_used}));

        displayMessage(this)
        
    } else{
        alert("You are not at the correct location");
    }

}
                        
                        
// Displays a message to the user, telling them that they have completed the challange
// There is 2 buttons in the message, one allows the user to play a minigame and the other allows the user to go back to the map
function displayMessage(object){
    // Sets the onject variable to the box, which is the parent of the object that the user clicked on
    object = object.parentElement;
    var message = document.createElement("div");
    message.id = "message";
    message.className = "message";
    message.innerHTML = "Challange Completed!! <br> <button class='minigame-button'>Play minigame</button>";

    //The coordinates to the bottle, bus stop or bin are stored in the pathButton

    message.Xcoordinates = (object.offsetLeft);
    message.Ycoordinates = (object.offsetTop);
    // Sets the position of the message box
    object.appendChild(message);


    // Creates a button that allows the user to play the minigame
    var minigameButton = document.querySelector('.minigame-button');
    minigameButton.addEventListener('click', minigame)
}

// A function that creates a small game where the user has to click on the bottles
// The user has 10 seconds to click on as many garbages as possible
function minigame(){
    const map = document.querySelector(".map");
    mapWidth = map.offsetWidth;
    mapHeight = map.offsetHeight;
    // Creates a box that contains the game
    var game = document.createElement("div");
    game.id = "game";
    game.className = "game";
    game.innerHTML = "Click on the trashbags as fast as you can! <br> <button class='start-button'>Start</button>";
    game.style.zIndex = '10000';
    var object = this.parentElement;
    object.appendChild(game);

    // Creates a button that starts the game
    var startButton = document.querySelector('.start-button');
    startButton.addEventListener('click', function() {
        // Create the overlay after starting the game
        const overlay = document.createElement('div');
        overlay.style.position = 'absolute';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.top = '0';
        overlay.style.zIndex = '500';
        //overlay.style.pointerEvents = 'none'; // Keep this line
        overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
        map.appendChild(overlay);
        // Creates a timer that counts down from 10
        var timer = document.createElement("div");
        timer.id = "timer";
        timer.className = "timer";
        timer.innerHTML = "10";
        game.appendChild(timer);
        var time = 10;
        var timerID = setInterval(function(){
            time--;
            timer.innerHTML = time;
            if (time == 0){
                var csrftoken = getCookie('csrftoken');
                clearInterval(timerID);
                game.innerHTML = "Game Over! <br> You clicked on " + score + " trashbags! <br>";
                garbage.remove();
                overlay.remove(); // Remove the overlay
                // Removes the garbage
                garbage.remove();
                var request = new XMLHttpRequest();
                request.open("POST", "/index", true);
                request.setRequestHeader("Content-Type", "application/json");
                request.setRequestHeader("X-CSRFToken", csrftoken);
                var extra_points = score * 10 + 250;
                request.send(JSON.stringify({points: extra_points}));
                location.reload();
            }
        }, 1000);

        // Creates a score counter
        var score = 0;
        var scoreCounter = document.createElement("div");
        scoreCounter.id = "scoreCounter";
        scoreCounter.className = "scoreCounter";
        scoreCounter.innerHTML = "Score: " + score;
        game.appendChild(scoreCounter);

        var garbage = document.createElement("div");
        garbage.id = "garbage";
        garbage.className = "garbage";
        garbage.style.left = Math.floor(Math.random() * mapWidth) + "px";
        garbage.style.top = Math.floor(Math.random() * mapHeight) + "px";
        garbage.style.zIndex = '10001'; // Set the zIndex of the garbage element
        garbage.addEventListener('click', function (e) {
            score++;
            scoreCounter.innerHTML = 'Score: ' + score;
          
            const map = document.querySelector('.map');
            const mapRect = map.getBoundingClientRect();
            const garbageRect = garbage.getBoundingClientRect();
          
            const garbage_x = garbageRect.left - mapRect.left + garbage.offsetWidth / 2;
            const garbage_y = garbageRect.top - mapRect.top + garbage.offsetHeight / 2;
          
            createParticles(garbage_x, garbage_y);
            garbage.style.left = Math.floor(Math.random() * mapWidth) + 'px';
            garbage.style.top = Math.floor(Math.random() * mapHeight) + 'px';
          });
        map.appendChild(garbage);
    });

        
}

function createParticles(x, y) {
    const particleCount = 30; // Number of particles to create
  
    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.classList.add('particle');

      // Apply the CSS properties in JavaScript
      particle.style.position = 'absolute';
      particle.style.width = '5px';
      particle.style.height = '5px';
      particle.style.backgroundColor = '#fff';
      particle.style.borderRadius = '50%';
      particle.style.zIndex = '1003';

      document.querySelector('.map').appendChild(particle);
  
      // Set the initial position of the particles
      particle.style.left = x + 'px';
      particle.style.top = y + 'px';
  
      // Generate random animation duration and angle
      const duration = Math.random() * 0.5 + 0.25; // Random duration between 0.25s and 0.75s
      const angle = Math.random() * Math.PI * 2; // Random angle
  
      // Calculate the particle's new position based on the angle and a random distance
      const distance = Math.random() * 50 + 25;
      const newX = x + Math.cos(angle) * distance;
      const newY = y + Math.sin(angle) * distance;
  
      // Animate the particle
      particle.animate(
        [
            { transform: `translate(0, 0)` },
            { transform: `translate(${newX - x}px, ${newY - y}px)` },
        ],
        {
          duration: duration * 1000,
          easing: 'linear',
          fill: 'forwards',
        }
      );
  
    //   // Remove the particle after the animation is completed
      setTimeout(() => {
        particle.remove();
      }, duration * 1500);
    }
  }
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
export { getCoordinates, createItems, getLocation, createMaze, startListeners, createBox, displayMessage, minigame, getCookie }


