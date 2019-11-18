# version 330

in vec3 newColor;
in vec2 texcoord;

uniform sampler2D ourtexture;

void main() {
	gl_FragColor = texture2D(ourtexture, texcoord);
	//gl_FragColor = vec4(0.5, 0.5, 0.5, 1.0);
}
