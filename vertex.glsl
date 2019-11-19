# version 330

in layout(location = 0) vec2 positions;
in layout(location = 1) vec3 colors;
in layout(location = 2) vec2 intexcoord;

out vec3 newColor;
out vec2 texcoord;

uniform vec2 screensize;

void main() {
	gl_Position = vec4(positions * vec2(2.0, -2.0) / screensize, 0.0, 1.0);
	newColor = colors;
	texcoord = intexcoord;
}
