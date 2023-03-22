import { getCoordinates } from '../app/static/global/js/maze.js';


test('should return the correct coordinates', () => {
    const lat = 50.735
    const lng = -3.535;

    const result = getCoordinates(lat, lng);

    expect(result).toStrictEqual({ x: '358.6568932624027px', y: '747.1221703464983px' });
});
