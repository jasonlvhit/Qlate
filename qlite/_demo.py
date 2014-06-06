class Template(object):
	def __init__(self, string):
		self.string = string
		self.body = []
		self.prev = 0
		self.curly = None
		self.result = []

	def generate(self, **kwargs):
		if not len(kwargs):
			raise Exception("type error")

		if self.body == []:
			self.parse()

		for node in self.body:
			if isinstance(node, TextNode):
				self.result.append(node.generate())
				continue
			if isinstance(node, ValueNode):
				self.result.append(node.generate(kwargs))

		return ''.join(self.result)

	def parse(self):
		while True:
			self.curly = self.string.find("{{", self.curly)
			if self.curly == -1:
				#raise Exception("Missing {{ ...")
				break

			end_brace = None
			end_brace = self.string.find("}}", self.curly)
			if not end_brace:
				continue
			if end_brace - self.curly == 0:
				raise Exception("Missing block content")

			self.body.append(TextNode(self.string[self.prev:self.curly]))

			block_content = self.string[self.curly + 2 :end_brace].strip()
			if not block_content:
				raise Exception("Missing block content")

			self.prev = end_brace + 2
			self.curly = end_brace + 2
			self.body.append(ValueNode(block_content))

class Node(object):
	def __init__(self, text):
		self.text = text

class TextNode(Node):
	def generate(self):
		return self.text

class ValueNode(Node):
	def generate(self, kwargs):
		if self.text not in kwargs.keys():
			return "{{" + self.text + "}}"

		return kwargs[self.text]


if __name__ == '__main__':
	t = Template("hello {{ name }}, hello {{ item }}")
	print(t.generate(name = "jason", item = "world"))

		
