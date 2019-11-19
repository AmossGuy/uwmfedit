# version 330

in vec2 texcoord;

uniform sampler2D ourtexture;

void main() {
	gl_FragColor = texture2D(ourtexture, texcoord);
}
