# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from braket.circuits import Circuit
from braket.devices import LocalSimulator


if __name__ == '__main__':
    device = LocalSimulator()
    bell = Circuit().h(range(2)).cnot(control=0, target=1)
    print(bell)
    print(device.run(bell, shots=100).result().measurement_counts)
