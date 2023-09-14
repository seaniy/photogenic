# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
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

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Sean & Carissa's Wedding Gallery! 👋")

    st.sidebar.success("Select a page above.")

    st.markdown(
        """
        📸 **Capture the moments, share the memories!** 📸

        We are beyond thrilled to have you with us on our special day, whether in person or in spirit. This platform is designed for all of us to weave a tapestry of memories together. 

        **Here's how it works:**
        1. **Snap & Upload:** Capture those candid moments, those heartwarming smiles, or any memory you'd love to share.
        2. **Browse & Relive:** Flip through the gallery and see the wedding through the eyes of our loved ones.

        Every photo tells a story, and we can't wait to see the story you tell. Thank you for being a part of our journey and for sharing these moments with us.

        **With all our love,**  
        Sean & Carissa ❤️

        **Take Note: You may find the upload & gallery pages on the sidebar menu. If you do not see a sidebar menu, please click on the arrow at the top left of the page.**
        """
    )

if __name__ == "__main__":
    run()
