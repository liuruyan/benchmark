#   Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from common_import import *


@benchmark_registry.register("masked_select")
class PaddleMaskedSelect(PaddleOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name="x", shape=config.x_shape, dtype=config.x_dtype)
        mask = self.variable(
            name="mask", shape=config.mask_shape, dtype=config.mask_dtype)
        result = paddle.masked_select(x, mask)

        self.feed_list = [x, mask]
        self.fetch_list = [result]
        if config.x_dtype in ["float16", "float32", "float64"]:
            if config.backward:
                self.append_gradients(result, [x])


@benchmark_registry.register("masked_select")
class TorchMaskedSelect(PytorchOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name="x", shape=config.x_shape, dtype=config.x_dtype)
        mask = self.variable(
            name="mask", shape=config.mask_shape, dtype=config.mask_dtype)
        result = torch.masked_select(input=x, mask=mask)

        self.feed_list = [x, mask]
        self.fetch_list = [result]
        # only Tensors of floating point and complex dtype can require gradients
        if config.x_dtype in ["float16", "float32", "float64"]:
            if config.backward:
                self.append_gradients(result, [x])


@benchmark_registry.register("masked_select")
class TFMaskedSelect(TensorflowOpBenchmarkBase):
    def build_graph(self, config):
        tensor = self.variable(
            name="x", shape=config.x_shape, dtype=config.x_dtype)
        mask = self.variable(
            name="mask", shape=config.x_shape, dtype=config.mask_dtype)
        result = tf.boolean_mask(tensor=tensor, mask=mask)

        self.feed_list = [tensor, mask]
        self.fetch_list = [result]
        if config.backward:
            self.append_gradients(result, [tensor])
