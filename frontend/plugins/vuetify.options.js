import colors from 'vuetify/es5/util/colors'

import {
  mdiAccount,
  mdiAccountPlus,
  mdiAlphabeticalVariant,
  mdiApi,
  mdiChartBubble,
  mdiChevronDown,
  mdiChevronUp,
  mdiCircleHalfFull,
  mdiCloseCircle,
  mdiEye,
  mdiEyeOff,
  mdiGmail,
  mdiHome,
  mdiImageOutline,
  mdiLinkedin,
  mdiLogin,
  mdiLogout,
  mdiMenu,
  mdiMinus,
  mdiRepeat,
  mdiWhatsapp,
} from '@mdi/js'

export default function () {
  return {
    icons: {
      iconfont: 'mdiSvg',
      values: {
        mdiAccount,
        mdiAccountPlus,
        mdiAlphabeticalVariant,
        mdiApi,
        mdiChartBubble,
        mdiChevronDown,
        mdiChevronUp,
        mdiCircleHalfFull,
        mdiCloseCircle,
        mdiEye,
        mdiEyeOff,
        mdiGmail,
        mdiHome,
        mdiImageOutline,
        mdiLinkedin,
        mdiLogin,
        mdiLogout,
        mdiMenu,
        mdiMinus,
        mdiRepeat,
        mdiWhatsapp,
      },
    },
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  }
}
