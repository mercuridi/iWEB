// Every test has been written by Dimitar Sivrev


// Import function from maze.js
const {
  getCoordinates,
  createElement,
  getLocation,
  createMaze,
  startListeners,
  createBox,
  displayPath,
  aStar,
  checkLocation,
} = require('../app/static/global/js/maze');

// Mock data to be used in the tests
const mockData = {
  latitude: 12.34,
  longitude: 56.78,
  user_id: 1,
  name: 'John Doe',
  address: '123 Main St',
};

// Mock functions to be used in the tests
const displayPathMock = jest.fn();
const getLocationMock = jest.fn();

// Tests the longitude and latitude to x and y coordinates converter
test('should return the correct coordinates', () => {
    const lat = 50.735
    const lng = -3.535;

    const result = getCoordinates(lat, lng);

    expect(result).toStrictEqual({ x: '358.6568932624027px', y: '747.1221703464983px' });
});

// Tests the function that creates the elements
describe('createElement', () => {
  beforeEach(() => {
    document.body.innerHTML = '<div class="map"></div>';
  });

  it('should create an element with the specified index, data, and className', () => {
    const index = 0;
    const data = [50.735, -3.534, 'Sample', 'Text'];
    const className = 'test-element';
    const createdElement = createElement(index, data, className);

    // Tests if the element isn't null
    expect(createdElement).toBeDefined();
    // Checks that the element's id has been created correctly
    expect(createdElement.id).toBe(`${className}-${index}`);
    // Checks that the element's class is correct
    expect(createdElement.className).toBe(className);
    // Checks the element's data [what floor, extra info] 
    expect(createdElement.textContent).toBe(`${data[2]} ${data[3]}`);
    // Checks that the longitude and latitude match
    expect(createdElement.latitude).toBe(data[0]);
    expect(createdElement.longitude).toBe(data[1]);
    // createElement makes the div's invisible, the buttons make them appear
    expect(createdElement.style.display).toBe('none');
    expect(createdElement.style.fontSize).toBe('0px');
  });
});

// Tests the function that maps the user's character
describe('getLocation', () => {
  // Set up the DOM for testing
  const originalGeolocation = global.navigator.geolocation;
  const originalPermissions = global.navigator.permissions;

  // Mock the geolocation and permissions objects
  beforeEach(() => {
    global.navigator.geolocation = {
      getCurrentPosition: jest.fn(),
      watchPosition: jest.fn(),
    };
    global.navigator.permissions = {
      query: jest.fn().mockResolvedValue({ state: 'granted' }),
    };
  });

  // Reset the geolocation and permissions objects after each test
  afterEach(() => {
    global.navigator.geolocation = originalGeolocation;
    global.navigator.permissions = originalPermissions;
  });

  // Tests the function when the user's location is not being tracked
  test('should call getCurrentPosition when track is false', async () => {
    await getLocation(false);

    expect(global.navigator.geolocation.getCurrentPosition).toHaveBeenCalledTimes(1);
    // watchPosition is the function that tracks the user's location
    expect(global.navigator.geolocation.watchPosition).toHaveBeenCalledTimes(0);
  });

  // Tests the function when the user's location is being tracked  
  test('should call watchPosition when track is true', async () => {
    await getLocation(true);

    expect(global.navigator.geolocation.getCurrentPosition).toHaveBeenCalledTimes(0);
    expect(global.navigator.geolocation.watchPosition).toHaveBeenCalledTimes(1);
  });
});

// Tests the function that creates the maze
describe('createMaze', () => {
  // Set up the DOM for testing
  document.body.innerHTML = `
    <div class="map">
    </div>
  `;

  test('should create the maze with the correct elements', () => {
    const map = [
      '#####',
      '#   #',
      '#####',
    ];

    createMaze(map);

    // Check that the maze has been created correctly
    // The maze is created by creating a div for each row
    // and then creating a div for each column
    // Therefore, the number of rows should be equal to the number of maze rows
    const mazeRows = document.querySelectorAll('.maze-row');
    expect(mazeRows.length).toBe(map.length);

   
  });
});

// Tests the function that starts the event listeners for the buttons and the items
describe('startListeners', () => {
  let originalAddEventListener;

  // Set up the DOM for testing
  beforeEach(() => {
    originalAddEventListener = window.Element.prototype.addEventListener;
    window.Element.prototype.addEventListener = jest.fn();

    document.body.innerHTML = `
      <div>
        <div class="bottle"></div>
        <div class="bus_stop"></div>
        <div class="bin"></div>
        <button class="water-fountain-button"></button>
        <button class="bus-stop-button"></button>
        <button class="bin-button"></button>
        <button class="track-button"></button>
      </div>
    `;
  });

  // Reset the addEventListener function after each test
  afterEach(() => {
    window.Element.prototype.addEventListener = originalAddEventListener;
  });

  test('should add event listeners to elements', () => {
    startListeners([]);

    expect(window.Element.prototype.addEventListener).toHaveBeenCalledTimes(7);
    expect(window.Element.prototype.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
  });
});

// Tests the function that creates the info box
describe('createBox', () => {
  test('should create an info box with the correct elements and event listeners', () => {

    // Set up the DOM for testing
    const context = { 
    id: mockData.user_id, 
    style: { left: '10px', top: '20px' },
    removeEventListener: jest.fn()
    };
    
    // Mock the functions that are called in createBox
    const mockMap = { appendChild: jest.fn() };
    document.querySelector = jest.fn().mockReturnValue(mockMap);

    const box = createBox.call(context, displayPathMock, getLocationMock);

    const closeButton = box.querySelector('.exitButton');
    expect(closeButton).not.toBeNull();

    const pathButton = box.querySelector('.pathButton');
    expect(pathButton).not.toBeNull();

    const checkButton = box.querySelector('.checkButton');
    expect(checkButton).not.toBeNull();
    checkButton.click();
  });
});

// Tests the A* algorithm
describe('aStar', () => {
  test('should find the shortest path in the maze', () => {
    const maze = [
      ['#', '#', '#', '#', '#'],
      ['#', '-', '#', '-', '#'],
      ['#', '-', '#', '-', '#'],
      ['#', '-', '-', '-', '#'],
      ['#', '#', '#', '#', '#'],
    ];

    const start = [1, 1];
    const end = [3, 3];
    const expectedPath = [
      [1, 1],
      [2, 1],
      [3, 1],
      [3, 2],
      [3, 3],
    ];

    const result = aStar(maze, start, end);
    expect(result).toEqual(expectedPath);
  });
});

// Tests the function that checks if the user is at the target
describe('checkLocation', () => {
  let alertMock;
  let displayMessageMock;
  let user;
  let target;

  beforeEach(() => {
    // Set up the mocks
    alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    displayMessageMock = jest.fn();

    // Set up the DOM elements
    user = document.createElement('div');
    user.classList.add('user');
    user.style.left = '100px';
    user.style.top = '100px';
    document.body.appendChild(user); // Add the user element to the document body

    target = document.createElement('div');
    target.id = 'target';
    target.dataset.Xcoordinates = '100';
    target.dataset.Ycoordinates = '100';

    // Set up the module functions
    window.displayMessage = displayMessageMock;
  });

  afterEach(() => {
    alertMock.mockRestore();
    document.body.removeChild(user); // Remove the user element from the document body
  });

  test('should alert user when not at the correct location', () => {
    user.style.left = '150px';
    user.style.top = '150px';
    const event = new MouseEvent('click');
    checkLocation.call(target, event);
    expect(displayMessageMock).not.toHaveBeenCalled();
    expect(alertMock).toHaveBeenCalledWith('You are not at the correct location');
  });
});
