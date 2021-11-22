#import numpy as np
from tqdm import tqdm
from PIL import Image
import torch.nn as nn
from torch.autograd import Variable
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torchvision
from Energy import Energy

class Predict:
	def __init__(self):
		# モデル定義
		self.model = models.resnet18(pretrained=True)
		self.model.fc = nn.Linear(512, 20) #10はクラスラベル数
		# パラメータの読み込み
		param = torch.load('dishes.pth',map_location=torch.device('cpu'))
		self.model.load_state_dict(param)
		# 評価モードにする
		self.model = self.model.eval()
		self.m = nn.Softmax(dim=1)
	
	def predict(self, image_name):
		image_file = 'pred_img/' #画像格納ファイル
		image_path = image_file + image_name
		image = self.image_loader(image_path)
		outputs = self.m(self.model(image))
		_, preds = torch.max(outputs.data, 1)
		return preds
		
	def image_loader(self, image_name):
		loader = transforms.Compose([ transforms.Resize(256),  # (256, 256) で切り抜く。
		transforms.CenterCrop(224),  # 画像の中心に合わせて、(224, 224) で切り抜く
		transforms.ToTensor(),  # テンソルにする。
		transforms.Normalize(
		mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
		),])
		image = Image.open(image_name).convert("RGB")
		image = loader(image)
		image = Variable(image, requires_grad=True)
		image = image.unsqueeze(0)  
		return image

"""	
pred = Predict()
idx = pred.predict('curry.jpg')

c = Energy()
print(c.dishLabel)
print(c.dishLabel[idx])
"""