# version 330

in layout(location = 0) vec2 positions;
in layout(location = 1) vec3 colors;

out vec3 newColor;

void main() {
	gl_Position = vec4(positions * vec2(1.0, -1.0), 0.0, 1.0);
	newColor = colors;
}
